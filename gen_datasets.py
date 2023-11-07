import subprocess
import os
import sys
sys.stdout.reconfigure(encoding='utf-16') #required on windows machines


#split documents by "NEWDOC [LABEL]", extract label to a variable
#Randomly put each doc in one of Dev, Test, Train (dev and test should be 25%, Train 50%)
#Generate labels file

def parse_file(file):
    
    pass

#Go through the dataset/Unicode folder
#open file
if __name__ == "__main__":
    for root, dirs, files in os.walk(r"/dataset/Unicode"):
        for file in files:
            if file.endswith(".txt"):
                text = open(file,encoding="utf-8")
                parse_file(text)
                text.close()


