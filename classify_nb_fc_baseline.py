import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, classification_report

import re

# n-gram tokenizer function
def tokenizer(text, n=1, startend=False, fullWord=False):
    
    if fullWord:
        return full_word_tokenizer(text)
    # Create n-character tokens from each word
    if startend:
        text = "<" + text + ">"
        text = re.sub(" ","> <",text)
    tokens = [text[i:i+n] for i in range(len(text) - n + 1)]
    return tokens

def full_word_tokenizer(text):
    return text.split()

# Read data function for the cuneiform file
def read_text_data(file_path):
    with open(file_path, encoding='utf16') as file:
        content = file.read()
    # Separate the data based on the 'NEWDOC' separator
    return [part.strip() for part in content.split('NEWDOC') if part.strip()]

def main():
    if len(sys.argv) < 8:
        print("Please specify the correct number of parameters. See description in code")
        sys.exit(1)

    # Command-line arguments for method and files
    classification_method = sys.argv[1]
    train_text_file = sys.argv[2]
    train_label_file = sys.argv[3]
    test_text_file = sys.argv[4]
    start_end =  sys.argv[5].lower() == 'true'
    full_word = sys.argv[6].lower() == 'true'
    

    # Read the training cuneiform data
    train_texts = read_text_data(train_text_file)

    # Read the training labels
    with open(train_label_file, encoding='utf16') as file:
        train_labels = [line.strip() for line in file.readlines()]

    # Read the test cuneiform data
    test_texts = read_text_data(test_text_file)

    # Vectorize the training and test data using the n-gram tokenizer
    
    
    grams = 3
    if len(sys.argv) == 8:
        grams = int(sys.argv[7])

    token_func = lambda text: tokenizer(text,grams,start_end,full_word)
    vectorizer = CountVectorizer(analyzer=token_func)

    X_train = vectorizer.fit_transform(train_texts)
    X_test = vectorizer.transform(test_texts)



    if classification_method == "nb":
        # Naive Bayes classifier
        clf = MultinomialNB()
        clf.fit(X_train, train_labels)
        predicted_labels = clf.predict(X_test)
    elif classification_method == "fc":
        # Most Frequent Class classifier
        clf = DummyClassifier(strategy="most_frequent")
        clf.fit(X_train, train_labels)
        predicted_labels = clf.predict(X_test)
    else:
        print("Please select a valid classification method: nb or fc")
        sys.exit(1)

    # Print out the predictions
    for prediction in predicted_labels:
        print(prediction)

if __name__ == "__main__":
    main()
