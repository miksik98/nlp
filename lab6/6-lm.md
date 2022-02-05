# Language modelling

The exercise shows how a language model may be used to solve word-prediction tasks and to generate text.


## Tasks

1. Read the documentation of [Language modelling in the Transformers](https://huggingface.co/transformers/task_summary.html#language-modeling) library.
1. Download three [Polish models](https://huggingface.co/models?filter=pl) from the Huggingface repository. 
1. Produce the predictions for the following sentences (use each model and check 5 predictions):
   1. (M) Warszawa to największe `[MASK]`.
   1. (D) Te zabawki należą do `[MASK]`.
   1. (C) Policjant przygląda się `[MASK]`.
   1. (B) Na środku skrzyżowania widać `[MASK]`.
   1. (N) Właściciel samochodu widział złodzieja z `[MASK]`.
   1. (Ms) Prezydent z premierem rozmawiali wczoraj o `[MASK]`.
   1. (W) Witaj drogi `[MASK]`.
1. Check the model predictions for the following sentences (using each model):
   1. Gdybym wiedział wtedy dokładnie to, co wiem teraz, to bym się nie `[MASK]`.
   1. Gdybym wiedziała wtedy dokładnie to, co wiem teraz, to bym się nie `[MASK]`.
1. Check the model predictions for the following sentences:
   1. `[MASK]` wrze w temperaturze 100 stopni, a zamarza w temperaturze 0 stopni Celsjusza.
   1. W wakacje odwiedziłem `[MASK]`, który jest stolicą Islandii.
   1. Informatyka na `[MASK]` należy do najlepszych kierunków w Polsce.
1. If you want to use causal language models such as PapuGaPT2 or plT5, you should change the last three examples to accomodate for the fact, that these
   models are better suited for causal language modelling.
3. Answer the following questions:
   1. Which of the models produced the best results?
   1. Was any of the models able to capture Polish grammar?
   1. Was any of the models able to capture long-distant relationships between the words?
   1. Was any of the models able to capture world knowledge?
   1. What are the most striking errors made by the models?

## Hints

1. Language modelling (LM) is a task concentrated on computing the probability distribution of words given a sequence of
   preceding words.
1. In the past the most popular LM were based on n-gram counting. The distribution of probability of the next word was
   approximated by the relative frequency of the last n-words, preceding this word. Usually n=3, since larger values
   resulted in extremely large datasets.
1. Many algorithms were devised to improve that probability estimates for infrequent words. Among them Kneser-Ney was
   the most popular.
1. SRI LM is the most popular toolkit for creating traditional language models.
1. At present recurrent neural networks, attention networks and transformers are the most popular neural-network
   architectures for creating LMs.
1. The largest LM currently is GPT-3 described in (mind the number of authors!) *Language Models are Few-Shot Learners*
   Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav
   Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon
   Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler,
   Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya
   Sutskever, Dario Amodei
