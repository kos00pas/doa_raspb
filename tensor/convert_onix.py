import tensorflow as tf
import tf2onnx
import onnx

# Load your Keras model
model = tf.keras.models.load_model('path/to/your/model.h5')

# Convert the model to a TensorFlow SavedModel format
tf.saved_model.save(model, "path/to/saved_model")

# Convert the TensorFlow SavedModel to ONNX
model_proto, _ = tf2onnx.convert.from_saved_model("path/to/saved_model", opset=13)

# Save the ONNX model
with open("path/to/your/model.onnx", "wb") as f:
    f.write(model_proto.SerializeToString())