#!/bin/bash
# run with: bash classify.sh this can take a while
# Most frequent class baseline
python classify_nb_fc_baseline.py fc dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 4 > Predictions/fc.txt


# Naive Bayes no start and end of word information
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 4 > Predictions/nb4.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 3 > Predictions/nb3.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 2 > Predictions/nb2.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 1 > Predictions/nb1.txt


# Naive Bayes start and end of word information
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 4 > Predictions/nbse4.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 3 > Predictions/nbse3.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 2 > Predictions/nbse2.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 1 > Predictions/nbse1.txt


# Naive Bayes full word model information
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False True 3 > Predictions/nbfw.txt


# SVM no start and end of word information
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 4 > Predictions/svm4.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 3 > Predictions/svm3.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 2 > Predictions/svm2.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 1 > Predictions/svm1.txt


# SVM start and end of word information
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 4 > Predictions/svmse4.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 3 > Predictions/svmse3.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 2 > Predictions/svmse2.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 1 > Predictions/svmse1.txt


# SVM full word model information
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False True 3 > Predictions/svmfw.txt

