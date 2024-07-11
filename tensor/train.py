import tensorflow as tf
from tensorflow.keras.datasets import mnist
import numpy as np

# Load MNIST dataset
(train_data, train_labels), (test_data, test_labels) = mnist.load_data()

# Normalize data to be in the range [0, 1]
train_data = train_data / 255.0
test_data = test_data / 255.0

# Flatten the images for the fully connected neural network
train_data = train_data.reshape(-1, 28 * 28)
test_data = test_data.reshape(-1, 28 * 28)
print("Checking for NaN values in training data:", np.isnan(train_data).any())
print("Checking for NaN values in training labels:", np.isnan(train_labels).any())

# Verify the data
print("Train data shape:", train_data.shape)
print("Test data shape:", test_data.shape)
print("Train data min value:", np.min(train_data))
print("Train data max value:", np.max(train_data))

# Define the model
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(28 * 28,)),
    tf.keras.layers.Dense(10, activation='softmax')
])


# Compile the model with appropriate loss function
model.compile(optimizer='sgd',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


# Train the model
model.fit(train_data, train_labels, epochs=5)

# Save the model
model.save('my_model.h5')
