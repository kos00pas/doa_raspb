import os
import threading
import time
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

import warnings

# Suppress numpy UserWarnings about subnormal floats
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")


class Classification_Window:
    def __init__(self, main_window, database):
        """
                Scope:          get access to main window and database
        """
        self.main_window = main_window
        self.DATA = database
        self.close_mfcc_event = threading.Event()  # Initialize the event

    def make_mfcc(self):
        print('making mfcc.....wait')
        time_start = time.time()
        last_second_data = np.concatenate(self.DATA.pending_c0)
        # Ensure the data type is int16
        last_second_data = last_second_data.astype(np.int16)

        # Extract exactly the last 16000 samples
        audio = last_second_data[-16000:]

        print(f'shape audio:{audio.shape}')
        audio_data = audio.flatten().astype(np.float32)
        # Parameters
        sr = self.DATA.resp4.RESPEAKER_RATE  # Assuming a sample rate from DATA object

        # Normalize the entire audio to a reference level (e.g., -20 dB)
        audio_data /= np.max(np.abs(audio_data))
        audio_data *= 10 ** (-20 / 20)  # Reference level at -20 dB

        # Compute MFCC
        n_fft = 2048
        hop_length = 512
        mfcc = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=40, n_fft=n_fft, hop_length=hop_length, fmax=8000)

        # Print the shape of the MFCC array
        print(f"MFCC shape: {mfcc.shape}")

        # Ensure the MFCC shape matches the model's expected input shape
        num_timesteps = 40  # Ensure this matches your model's expected input shape
        num_mfcc = 32  # Ensure this matches your model's expected input shape

  
        X_test = mfcc.reshape(1, num_timesteps, num_mfcc, 1)

        # Set the tensor to point to the input data to be inferred
        self.DATA.cnn_interpreter.set_tensor(self.DATA.cnn_input_details[0]['index'], X_test.astype(np.float32))

        # Run the inference
        self.DATA.cnn_interpreter.invoke()

        # Extract the output data from the interpreter
        predictions = self.DATA.cnn_interpreter.get_tensor(self.DATA.cnn_output_details[0]['index'])

        # Convert predictions to binary class labels using the threshold
        class_predictions = (predictions > self.DATA.cnn_threshold).astype(int).flatten().tolist()
        print(f"Predictions: {class_predictions}")
        # self.main_window.prediction_label.config(font="bold",text=f'Prediction: {str(class_predictions)}')

        # Save the MFCC and signal to CSV
        the_now_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        base_dir = os.getcwd()
        save_dir = os.path.join(base_dir, "MFCC_SIGNAL_saves", the_now_time)
        os.makedirs(save_dir, exist_ok=True)
        self.DATA.Save_mfcc_csv(mfcc, save_dir)
        self.DATA.Save_signal_csv(audio_data, save_dir)
        time_end = time.time()
        elapsed_time = time_end - time_start
        print(f'Time taken for MFCC computation: {elapsed_time} seconds')
