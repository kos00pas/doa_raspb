import numpy as np
import tflite_runtime.interpreter as tflite

# Load TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Prepare input data (example using a single sample from MNIST)
sample_input = np.array(test_data[0:1], dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], sample_input)

# Run the inference
interpreter.invoke()

# Get the output
output_data = interpreter.get_tensor(output_details[0]['index'])
print(output_data)
