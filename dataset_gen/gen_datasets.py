import subprocess
import os
import sys
import re
import random
sys.stdout.reconfigure(encoding='utf-16') #required on windows machines


#split documents by "NEWDOC [LABEL]", extract label to a variable
#Randomly put each doc in one of Dev, Test, Train (dev and test should be 25%, Train 50%)
#Generate labels file

def parse_file(file,trainData,trainLabels,devData,devLabels,testData,testLabels):

    #Originally planned to extract the label from the start of every doc and use that, but for time's sake,
    # we just the first label we find and discard the rest
    z = re.search(r"NEWDOC\s(\w+)",file)
    label = z.groups()[0]
    g = re.sub(label,"",file)

    
    docs = re.split("NEWDOC",g)#file) #\s+(\w+)
    print(len(docs))
    for i,doc in enumerate(docs):
        #no whitespace documents, these can happen when only annotation and/or words not in the sign list appear
        x = re.sub("[\s\n]+","",doc)
        if x == "":
            continue
        #distribute the data, write it to the output files
        #0,1 will be training, 2 will be dev, 3 will be test
        category = random.randint(0,3) 
        if category == 0 or category == 1:
            trainData.write("NEWDOC\n")
            trainData.write(doc+"\n")
            trainLabels.write(label+"\n")
        elif category == 2:
            devData.write("NEWDOC\n")
            devData.write(doc+"\n")
            devLabels.write(label+"\n")
        elif category == 3:
            testData.write("NEWDOC\n")
            testData.write(doc+"\n")
            testLabels.write(label+"\n")       
    

#Go through the dataset/Unicode folder, distribute the documents to training, dev, and testing sets
if __name__ == "__main__":
    mode = 'w'
    with(
    open(r"./dataset/Model/train.data.txt",mode,encoding='utf16') as x,
    open(r"./dataset/Model/train.label.txt",mode,encoding='utf16') as y,
    open(r"./dataset/Model/dev.data.txt",mode,encoding='utf16') as z,
    open(r"./dataset/Model/dev.label.txt",mode,encoding='utf16') as w,
    open(r"./dataset/Model/test.data.txt",mode,encoding='utf16') as j,
    open(r"./dataset/Model/test.label.txt",mode,encoding='utf16') as k):
        #Probably the most fragile part of the project, python is picky with the encodings
        # and syntax
        #note to self, using "" instead of '' breaks open syntax?
        for root, dirs, files in os.walk(r"./dataset/Unicode"):
            for file in files:
                if file.endswith(".txt"):
                    text = open("./dataset/Unicode/"+file,encoding='utf-16') #as s:
                    print(file)
                    parse_file(text.read(),x,y,z,w,j,k)
