#Score everything, run with: & "./score.ps1"
python score_baseline.py dataset/Model/test.label.txt Predictions/fc.txt > Results/fc.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb1.txt > Results/nb1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb2.txt > Results/nb2.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb3.txt > Results/nb3.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nb4.txt > Results/nb4.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nbse1.txt > Results/nbse1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nbse2.txt > Results/nbse2.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nbse3.txt > Results/nbse3.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nbse4.txt > Results/nbse4.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/nbfw.txt > Results/nbfw.txt 
python score_baseline.py dataset/Model/test.label.txt Predictions/svm1.txt > Results/svm1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm2.txt > Results/svm2.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm3.txt > Results/svm3.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svm4.txt > Results/svm4.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svmse1.txt > Results/svmse1.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svmse2.txt > Results/svmse2.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svmse3.txt > Results/svmse3.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svmse4.txt > Results/svmse4.txt
python score_baseline.py dataset/Model/test.label.txt Predictions/svmfw.txt > Results/svmfw.txt 