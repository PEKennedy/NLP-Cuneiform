import sys
from sklearn.metrics import accuracy_score, classification_report

# To call: python scores.py real_label.txt predicted_label.txt
# Note that real label is in utf16 and predicted label in utf8

def read_labels(file_path, encoding='utf-16'):#'utf-16'): #utf-16
    with open(file_path, 'r', encoding=encoding) as file:
        labels = [line.strip() for line in file]
    return labels

def calculate_metrics(real_labels, predicted_labels):
    accuracy = accuracy_score(real_labels, predicted_labels)
    report = classification_report(real_labels, predicted_labels, output_dict=True)
    macro_f1 = report['macro avg']['f1-score']
    precision = report['macro avg']['precision']
    recall = report['macro avg']['recall']
    return accuracy, precision, recall, macro_f1

def main():
    if len(sys.argv) != 3:
        print("Specify the correct number of parameters. See description in code")
        sys.exit(1)

    real_labels_file = sys.argv[1]
    predicted_labels_file = sys.argv[2]

    real_labels = read_labels(real_labels_file, encoding='utf-16')
    predicted_labels = read_labels(predicted_labels_file,encoding='utf-8') #utf-16 on windows #, encoding='utf-8'

    accuracy, precision, recall, macro_f1 = calculate_metrics(real_labels, predicted_labels)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro Precision: {precision:.4f}")
    print(f"Macro Recall: {recall:.4f}")
    print(f"Macro F1 Score: {macro_f1:.4f}")

if __name__ == "__main__":
    main()
