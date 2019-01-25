# Parts-of-Speech-Tagging-using-Hidden-Markov-Model
HMM POS tagger using Python that can be used to tag any natural language. The model is trained to learn the parameters such as transition and emission probabilities using which the Viterbi algorithm tags the unseen data.
The training data are provided tokenized and tagged. The test data will be provided tokenized, and the tagger will add the tags
The tagged training data should in the word/TAG format, with words separated by spaces and each sentence on a new line

There are two programs
hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data
The learning program will be invoked in the following way:
> python hmmlearn.py /path/to/input
The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt.

The tagging program will be invoked in the following way:
> python hmmdecode.py /path/to/input
The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt

