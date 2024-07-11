import numpy as np
import tensorflow as tf
import random

# Load the saved model
model = tf.keras.models.load_model('my_model.h5')

# Generate synthetic data to simulate MNIST dataset
def generate_synthetic_mnist_data(num_samples=10000, img_size=28*28, num_classes=10):
    images = np.random.randint(0, 255, size=(num_samples, img_size)).astype('float32')
    labels = np.random.randint(num_classes, size=(num_samples,))
    return images, labels

# Generate synthetic MNIST test dataset
images, labels = generate_synthetic_mnist_data()

# Preprocess the data
test_data = images / 255.0
test_labels = labels

# Using a random sample from the test data
index = random.randrange(0, len(test_data))
input_data = np.array(test_data[index:index+1], dtype=np.float32)

# Validate input data
print("Input data min value:", np.min(input_data))
print("Input data max value:", np.max(input_data))
print("Input data shape:", input_data.shape)
print("Input data:", input_data)

# Run inference using the model
output_data = model.predict(input_data)
print("Output data:", output_data)
print("Actual label:", test_labels[index])
