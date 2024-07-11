import numpy as np
import tflite_runtime.interpreter as tflite
import random

# Generate synthetic data to simulate MNIST dataset
def generate_synthetic_mnist_data(num_samples=10000, img_size=28*28, num_classes=10):
    images = np.random.randint(0, 255, size=(num_samples, img_size)).astype('float32')
    labels = np.random.randint(0, num_classes, size=(num_samples,))
    return images, labels

# Generate synthetic MNIST test dataset
images, labels = generate_synthetic_mnist_data()

# Preprocess the data
test_data = images / 255.0
test_labels = labels

# Load TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Print input details for debugging
print("Input details:", input_details)

# Using a random sample from the test data
index = random.randrange(0, len(test_data))
input_data = np.array(test_data[index:index+1], dtype=np.float32)

# Reshape input data to match model's expected input shape (1, 28, 28)
input_data = input_data.reshape((1, 28, 28))

# Validate input data
print("Input data min value:", np.min(input_data))
print("Input data max value:", np.max(input_data))
print("Input data shape:", input_data.shape)
print("Input data:", input_data)

# Ensure the input data is in the correct range
if np.any(input_data < 0) or np.any(input_data > 1):
    print("Error: Input data out of expected range [0, 1].")
else:
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run the inference
    interpreter.invoke()

    # Get the output
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print("Output data:", output_data)
    print("Actual label:", test_labels[index])
