# Neural search for question answering

The exercise introduces the problem of factual question answering. This part concentrates on the methods for retrieving
the content of documents that potentialy might be useful for answering the question. We compare sparse text
representations (e.g. ElasticSearch default behaviour), with dense text representations (e.g. Dense Passage Retriever
bi-encoder neural model).

## Tasks

1. Read the documentation of the [document store](https://haystack.deepset.ai/components/v1.0.0/document-store) and
   the [document retriever](https://haystack.deepset.ai/components/v1.0.0/retriever) in the 
   [Haystack framework](https://haystack.deepset.ai/overview/intro).
1. Install Haystack framework. You may need to used [this fork](https://github.com/apohllo/haystack/tree/use-auto-tokenizer-by-default) 
   to get support for Polish QA models.
3. Configure one document store based on ElasticSearch and another document store based on Faiss supported by DPR:
   1. The ES store should properly process Polish documents.
   2. For DPR you should use [enelpol/czywiesz-question](https://huggingface.co/enelpol/czywiesz-question) and 
      [enelpol/czywiesz-context](https://huggingface.co/enelpol/czywiesz-context) encoders.
   3. **Warning:** Make sure to used models uploaded past 21st of December 2021, since the first model version included a bug.
4. Pre-process all documents from the set of Polish bills (used in the previous exercises), but splitting them into
   individual articles: 
   1. You can apply a simple heuristic that searches for `Art.` at the beginnign of the processed line, to identify the passages. 
   2. Assing identifiers to the passages by combining the file name with the article id.
   3. There might be repeated identifiers, since we use a heuristic. You should ignore that problem - just make sure
      that you load only one passage with a specific id.
3. Load the passages from previous point to the document stores described in point 2.
4. Randomly select 100 passages that do not describe an amendment (you can manually reject the amendments). 
5. Invent 30 factual questions based directly on 30 distinct passages that you have selected. The larger number of
   randomly selected passages should allow to skip those that are hard for inventing a question for them.
6. For the following passage:
   ```
                                          Art. 12.
      1. Prawo do uzyskania patentu na wynalazek, prawa ochronnego na wzór użytkowy
        albo prawa z rejestracji wzoru przemysłowego jest zbywalne i podlega
        dziedziczeniu.
      2. Umowa o przeniesienie prawa, o którym mowa w ust. 1, wymaga, pod rygorem
        nieważności, zachowania formy pisemnej.
   ```
   The following questions might be devised:
   1. Jakiej formy wymaga umowa przeniesienie prawa ochronnego na wzór użytkowy?
   2. Czy prawo z rejestracji wzoru przemysłowego jest dziedziczne?
   3. Czy prawo do uzyskania patentu na wynalazek może być sprzedane?
7. The following requirements are applied to the questions from the previous point:
   1. Each passage must have up to one question in the dataset.
   2. The questions, the ids of the passages and the content of the passages have to be stored in CSV file, with the
      following format: `passage_id`, `question`, `passage`.
   3. The question have to be factual, i.e. the passage need to include all information necessary to answer it. This
      means that general knowlege or knowledge encoded in different aricles or bills (even though there is a pointer in 
      the text to such regulations) must not be required to answer the question. Yet if one paragraph (point, letter, tired) 
      of the article relates to the other paragraph (point, letter, tired), such question is ok. In fact the first 
      question above is based on the reference between the second and the first paragraph.
   4. For binary questions (yes/no): make sure the number of questions with **yes** answer is similar to the questions
      with **no** answer.
   5. The question should be related to the law. Questions asking for the lenght of the passage, the sum of digits in the passage
      or the number of capital leters in the passage are not law-related.
8. Use the set of questions defined in the previous point to assess the performance of the document stores:
   1. Make a query based on the question to each store.
   2. Return 3 top document for the questions.
   3. Assess the validity of the returned passages. It is possible that more than one passage contains the answer to the
      question.
   4. If there are passages containg the answer to the given question, append those passages (with the question, passage
      id and passage content) to the reference file.
9. Compare the performance of the data stores using the following metrics: Pr@1, Rc@1, Pr@3, Rc@3.
10. Make a pull request to the repository: https://github.com/apohllo/simple-legal-questions-pl containing the file with the questions.
10. Answer the following questions:
    1. Which of the document stores performs better? Take into account the different metrics enumerated in the previous
       point.
    2. Which of the document stores is faster?
    3. Try to determine the other pros and cons of using sparse and dense document retrieval models.
   

## Hints

1. Haystack is a framework for buliding question answering applications.
2. Sparse document retrieval is based on sparse vector models, i.e. models based on bag of words. ElasticSearch typical
   usage is based on sparse document model.
3. Dense document retrieval is based on dense vector models provided by neural networks. These dense vectors might be 
   generated directly, by e.g. avaraging the vectors of word embeddings belonging to a given text fragment. Yet such
   models performance is inferior to sparse models.
4. More sophisticated models are trained directly on the document retrieval task. E.g. [DPR](https://arxiv.org/abs/2004.04906)
   uses a bi-encoder architecture that has a separate neural network for encoding the question and for encoding the passage.
   These netowrks are trained to maximise the dot-product of the vectors produced by each of the networks.
5. Using dense vector representation requires computing the dense vectors for all passages in the dataset. 
   These vectors might be stored in document stores such as [FAISS](https://github.com/facebookresearch/faiss) for faster retrieval, 
   especially when the dataset is very large (does not fit into memory).
6. Pr@n and Rc@n meen *precision at n* and *recall at n*. They are computed by retrieving `n` top documents and
   computing the metrics in a regular way. E.g. if among 3 retrieved documents there are 2 valid documents out of 5, 
   Pr@3 is 2/3 = 66% and Rc@3 is 2/5 = 40%.
