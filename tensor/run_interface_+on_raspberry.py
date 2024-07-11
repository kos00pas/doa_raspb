import numpy as np
from tflite_runtime.interpreter import Interpreter

# Load the trained TFLite model
interpreter = Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Synthetic test data
test_data = np.random.rand(1, 28, 28).astype(np.float32)
test_data = test_data / 255.0  # Normalize the data
test_data = test_data.reshape((1, 784))  # Flatten the data to match input shape

# Print input details for debugging
print("Input details:", input_details)
print("Input data min value:", np.min(test_data))
print("Input data max value:", np.max(test_data))
print("Input data shape:", test_data.shape)
print("Input data:", test_data)

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], test_data)

# Run inference
interpreter.invoke()

# Get the output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])
print("Output data:", output_data)

# For comparison, use the actual labels (if any)
# Here we use a placeholder label since we are using synthetic data
actual_label = 5  # This is just a placeholder
print("Actual label:", actual_label)
