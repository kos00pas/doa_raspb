import onnxruntime as ort
import numpy as np

# Load the ONNX model
session = ort.InferenceSession('path/to/your/model.onnx')

# Get model input details
input_name = session.get_inputs()[0].name
input_shape = session.get_inputs()[0].shape
input_type = session.get_inputs()[0].type

# Prepare input data
# Example: If the model expects an image, you might use OpenCV or PIL to load and preprocess the image
# Here, we assume the input is a NumPy array
input_data = np.random.rand(*input_shape).astype(np.float32)

# Run inference
results = session.run(None, {input_name: input_data})

# Output the results
print("Model output:", results)