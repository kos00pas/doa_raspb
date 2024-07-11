import tensorflow as tf

# Load your trained model
model = tf.keras.models.load_model('my_model.h5')

# Convert to TensorFlow Lite model
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the converted model
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
