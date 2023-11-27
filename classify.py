import tensorflow as tf
import numpy as np

def read_data(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = file.read().split('NEWDOC')[1:]
    return data

def load_model_and_encoder(model_path):
    model = tf.keras.models.load_model(model_path)
    encoder = model.layers[0]
    return model, encoder


def predict_and_save_labels(model, preprocessed_test_data, label_mapping, output_file_path):
    predictions = model.predict(preprocessed_test_data)
    predicted_labels = np.argmax(predictions, axis=1)

    with open(output_file_path, 'w') as output_file:
        for predicted_label in predicted_labels:
            label_word = list(label_mapping.keys())[predicted_label]
            output_file.write(f"{label_word}\n")

    print(f"Predictions written to {output_file_path}")

def main():
    # Define file paths
    test_data_path = 'dataset/Model/Model/test.data.txt'
    model_path = 'modelworks'
    output_file_path = 'RNN_predictions.txt'

    # Read test data
    test_data = read_data(test_data_path)

    # Load model and encoder
    model, encoder = load_model_and_encoder(model_path)

    # Preprocess test data
    predict_test_data_np = np.array(test_data)
    # Preprocess predict_test_data
    preprocessed_test_data = encoder(test_data).numpy()

    # Define label mapping
    label_mapping = {'ADMIN': 0, 'CONTRACT': 1, 'LEGAL': 2, 'LETTER': 3, 'LEXICAL': 4, 'LITERARY': 5, 'MEDICAL': 6, 'OFFICIAL': 7}

    # Predict and save labels
    predict_and_save_labels(model, test_data, label_mapping, output_file_path)

if __name__ == "__main__":
    main()