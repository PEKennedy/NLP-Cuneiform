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
    #Add all labels to an array
    #print(file)
    #docHeaders = re.finditer(r"NEWDOC (\w+)",file)
    #print(docHeaders)
    z = re.search(r"NEWDOC\s(\w+)",file)
    label = z.groups()[0]
    g = re.sub(label,"",file)
    """for header in docHeaders:
        #print(header)
        label = header.groups()[0]
        labels.append(label)
    print(len(labels))"""
    #print(labels)
    
    docs = re.split("NEWDOC",g)#file) #\s+(\w+)
    print(len(docs))
    for i,doc in enumerate(docs):
        #no whitespace documents
        #x = re.sub("OFFICIAL","",doc)
        x = re.sub("[\s\n]+","",doc)
        if x == "":
            #del labels[i]
            continue
        #doc = re.sub("OFFICIAL")
        #distribute the data
        #0,1 will be training, 2 will be dev, 3 will be test
        category = random.randint(0,3) 
        #NVM, try modulo
        #category = i%4
        if category == 0 or category == 1:
            trainData.write("NEWDOC\n")
            trainData.write(doc+"\n")
            trainLabels.write(label+"\n")#s[i])
        elif category == 2:
            devData.write("NEWDOC\n")
            devData.write(doc+"\n")
            devLabels.write(label+"\n")#s[i])
        elif category == 3:
            testData.write("NEWDOC\n")
            testData.write(doc+"\n")
            testLabels.write(label+"\n")#s[i])         
    

#Go through the dataset/Unicode folder
#open file
#,encoding="utf-8"
if __name__ == "__main__":
    mode = 'w'
    with(
    open(r"./dataset/Model/train.data.txt",mode,encoding='utf16') as x,
    open(r"./dataset/Model/train.label.txt",mode,encoding='utf16') as y,
    open(r"./dataset/Model/dev.data.txt",mode,encoding='utf16') as z,
    open(r"./dataset/Model/dev.label.txt",mode,encoding='utf16') as w,
    open(r"./dataset/Model/test.data.txt",mode,encoding='utf16') as j,
    open(r"./dataset/Model/test.label.txt",mode,encoding='utf16') as k):
        """trainData = x.read()
        trainLabels = y.read()
        devData = z.read()
        devLabels = w.read()
        testData = j.read()
        testLabels = k.read()"""
        #print(j[0])
        #note to self, using "" instead of '' breaks open syntax?
        for root, dirs, files in os.walk(r"./dataset/Unicode"):
            for file in files: #
                if file.endswith(".txt"):#,"rb"
                    #with open("./dataset/Unicode/"+file,"rb") as s:
                        #text = s.read()
                        #,encoding="utf-8"
                    #,'r'
                    #,errors="ignore"
                    text = open("./dataset/Unicode/"+file,encoding='utf-16') #as s:
                        #text = s.read()
                        #print(text)
                    print(file)
                    parse_file(text.read(),x,y,z,w,j,k)
                                   #,trainData,trainLabels,devData,devLabels,testData,testLabels)
                        #text.close()

    """trainData.close()
    trainLabels.close()
    devData.close()
    devLabels.close()
    testData.close()
    testLabels.close()"""
