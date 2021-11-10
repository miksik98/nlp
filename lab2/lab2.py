from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import os
import numpy as np

es = Elasticsearch()

# es.indices.delete('my_index')

try:
    es.indices.get('my_index')
except NotFoundError as e:
    es.indices.create(
        index="my_index",
        body={
            "settings": {
                "analysis": {
                    "analyzer": {
                        "default": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "nlp_synonyms",
                                "morfologik_stem",
                                "lowercase",
                            ]
                        }
                    },
                    "filter": {
                        "nlp_synonyms": {
                            "type": "synonym",
                            "synonyms": [
                                "kpk,kodeks postępowania karnego",
                                "kpc,kodeks postępowania cywilnego",
                                "kk,kodeks karny",
                                "kc,kodeks cywilny",
                            ]
                        }
                    }
                }
            },
        }
    )

    ustawy_path = '../ustawy'
    for filename in os.listdir(ustawy_path):
        with open(ustawy_path + '/' + filename, 'r', encoding='utf8') as f:
            content = f.read()
            body = {"content": content}
            es.create(index="my_index", id=filename, body=body)

print("docs number with ustawa |", es.search(
    index="my_index",
    body={
        "query": {
            "match": {
                "content": {
                    "query": "ustawa"
                }
            }
        }
    }
)["hits"]["total"])

result = es.termvectors(index="my_index",
                        id="2001_1382.txt",
                        body={
                            "fields": ["content"],
                            "term_statistics": True,
                            "field_statistics": True
                        })["term_vectors"]["content"]["terms"]["ustawa"]["ttf"]

print("ilość wystąpień ustawa | ", result)

print("kodeks postępowania cywilnego |", es.search(
    index="my_index",
    body={
        "query": {
            "match_phrase": {
                "content": {
                    "query": "kodeks postępowania cywilnego"
                }
            }
        }
    }
)["hits"]["total"])

print("wchodzi w życie |", es.search(
    index="my_index",
    body={
        "query": {
            "match_phrase": {
                "content": {
                    "query": "wchodzi w życie",
                    "slop": 2
                }
            }
        },
    }
)["hits"]["total"])

x = es.search(
    index="my_index",
    body={
        "query": {
            "match": {
                "content": {
                    "query": "konstytucja",
                }
            }
        },
        "highlight": {
            "fields": {
                "content": {}
            },
            "boundary_scanner": "sentence",
            "number_of_fragments": 3,
            "order": "score"
        }
    }
)["hits"]
top = [[e['_score'], e['_id'], e['highlight']['content']] for e in sorted(x['hits'], key=lambda e: -e['_score'])][:10]
top = np.array(top)
print("10 documents the most relevant for phrase konstytucja:\n", top[:, :2])
print("Excerpts:\n", top[:, 1:])
