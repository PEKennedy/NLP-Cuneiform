import tensorflow as tf
import numpy as np

def read_data(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = file.read().split('NEWDOC')[1:]
    return data

def read_labels(file_path, label_mapping):
    with open(file_path, 'r', encoding='utf-16') as file:
        labels = file.read().split('\n')
    return np.array([label_mapping[label] for label in labels if label in label_mapping])

def create_tf_dataset(data, labels, batch_size=32, shuffle_buffer_size=10000):
    dataset = tf.data.Dataset.from_tensor_slices((data, labels))
    dataset = dataset.shuffle(shuffle_buffer_size).batch(batch_size)
    return dataset

def create_encoder(train_dataset, max_tokens=10000, output_sequence_length=250):
    encoder = tf.keras.layers.TextVectorization(max_tokens=max_tokens, output_mode='int', output_sequence_length=output_sequence_length)
    encoder.adapt(train_dataset.map(lambda text, _: tf.strings.lower(text)))
    return encoder

def create_model(encoder):
    model = tf.keras.Sequential([
        encoder,
        tf.keras.layers.Embedding(len(encoder.get_vocabulary()), 64, mask_zero=True),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(8, activation='softmax')
    ])
    return model

def train_model(model, train_dataset, validation_dataset=None):
    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        optimizer=tf.keras.optimizers.Adam(),
        metrics=['accuracy']
    )
    
    history = model.fit(
        train_dataset,
        epochs=5,
        validation_data=validation_dataset,
    )
    
    return model, history

def main():
    # File paths
    train_data_path = 'dataset/Model/Model/train.data.txt'
    train_label_path = 'dataset/Model/Model/train.label.txt'
    dev_data_path = 'dataset/Model/Model/dev.data.txt'
    dev_label_path = 'dataset/Model/Model/dev.label.txt'
    output_model_path = 'RNNmodel'

    # Define label mapping
    label_mapping = {'ADMIN': 0, 'CONTRACT': 1, 'LEGAL': 2, 'LETTER': 3, 'LEXICAL': 4, 'LITERARY': 5, 'MEDICAL': 6, 'OFFICIAL': 7}

    # Read data and labels
    train_data = read_data(train_data_path)
    train_labels = read_labels(train_label_path, label_mapping)
    dev_data = read_data(dev_data_path)
    dev_labels = read_labels(dev_label_path, label_mapping)

    # Create TensorFlow datasets
    train_dataset = create_tf_dataset(train_data, train_labels)
    dev_dataset = create_tf_dataset(dev_data, dev_labels)

    # Create encoder for preprocessing
    encoder = create_encoder(train_dataset)

    # Create the model
    model = create_model(encoder)

    # Model summary
    model.summary()

    # Train the model
    trained_model, history = train_model(model, train_dataset, validation_dataset=dev_dataset)

    # Save the model
    trained_model.save(output_model_path, save_format='tf')
    print(f"Model saved as {output_model_path}")

if __name__ == "__main__":
    main()