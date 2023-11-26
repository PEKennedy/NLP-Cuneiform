import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, classification_report

# n-gram tokenizer function
def ngram_tokenizer(text, n=3):
    # Create n-character tokens from each word
    tokens = [text[i:i+n] for i in range(len(text) - n + 1)]
    return tokens

# Read data function for the cuneiform file
def read_text_data(file_path):
    with open(file_path, encoding='utf16') as file:
        content = file.read()
    # Separate the data based on the 'NEWDOC' separator
    return [part.strip() for part in content.split('NEWDOC') if part.strip()]

def main():
    if len(sys.argv) < 5:
        print("Please specify the correct number of parameters. See description in code")
        sys.exit(1)

    # Command-line arguments for method and files
    classification_method = sys.argv[1]
    train_text_file = sys.argv[2]
    train_label_file = sys.argv[3]
    test_text_file = sys.argv[4]

    # Read the training cuneiform data
    train_texts = read_text_data(train_text_file)

    # Read the training labels
    with open(train_label_file, encoding='utf16') as file:
        train_labels = [line.strip() for line in file.readlines()]

    # Read the test cuneiform data
    test_texts = read_text_data(test_text_file)

    # Vectorize the training and test data using the n-gram tokenizer
    vectorizer = CountVectorizer(analyzer=ngram_tokenizer)
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
