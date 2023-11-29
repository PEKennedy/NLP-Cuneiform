# NLP-Cuneiform
Uses Natural Language Processing to make a prediction about a cuneiform document
Made for CS4765 Natural Language Processing

## About

- Scripts to compile a custom dataset are located in /dataset_gen, check out its readme for building
 the dataset from the CDLI corpus and the folder's scripts.
- A set of documents sorted into training, development, and testing subsets, labelled
is already made under dataset/Model.zip.
- /Results contains the results of various models
- classify.py implements the most frequent class baseline classifier, Naive Bayes, and SVM.
- /RNNmodel is a keras/tensorflow model built on the dataset

## Usage

- To run the baseline and benchmark classifiers, create a `/Predictions` folder, and use `./classify.sh` then `./score.sh`. This will build and score all the baseline and benchmark classifiers. The Powershell files are equivalent to the bash files.
- To train or score a specific benchmark or baseline, check classify_benchmark.py for the parameters,
 and the shell files for examples of the commands themselves.
- To train the RNN model ....
- To use the RNN model ....