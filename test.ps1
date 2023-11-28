# Most frequent class baseline
python classify_nb_fc_baseline.py fc dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 4 > Predictions/fc.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/fc.txt > Results/fc.txt

# Naive Bayes no start and end of word information
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 4 > Predictions/nb4.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 3 > Predictions/nb3.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 2 > Predictions/nb2.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 1 > Predictions/nb1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb1.txt > Results/nb1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb2.txt > Results/nb2.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb3.txt > Results/nb3.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb4.txt > Results/nb4.txt

# Naive Bayes start and end of word information
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 4 > Predictions/nbse4.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 3 > Predictions/nbse3.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 2 > Predictions/nbse2.txt
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 1 > Predictions/nbse1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb1se.txt > Results/nb1se.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb2se.txt > Results/nb2se.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb3se.txt > Results/nb3se.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb4se.txt > Results/nb4se.txt

# Naive Bayes full word model information
python classify_nb_fc_baseline.py nb dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False True 3 > Predictions/nbfw.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nbfw.txt > Results/nbfw.txt 

# SVM no start and end of word information
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 4 > Predictions/svm4.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 3 > Predictions/svm3.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 2 > Predictions/svm2.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False False 1 > Predictions/svm1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm1.txt > Results/svm1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm2.txt > Results/svm2.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm3.txt > Results/svm3.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm4.txt > Results/svm4.txt

# SVM start and end of word information
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 4 > Predictions/svmse4.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 3 > Predictions/svmse3.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 2 > Predictions/svmse2.txt
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt True False 1 > Predictions/svmse1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm1se.txt > Results/svm1se.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm2se.txt > Results/svm2se.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm3se.txt > Results/svm3se.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm4se.txt > Results/svm4se.txt

# SVM full word model information
python classify_nb_fc_baseline.py svm dataset/Model/train.data.txt dataset/Model/train.label.txt dataset/Model/test.data.txt False True 3 > Predictions/svmfw.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svmfw.txt > Results/svmfw.txt 

