import os
import threading
import time
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt


class Classification_Window:
    def __init__(self, main_window, database):
        """
                Scope:          get access to main window and database
        """
        self.main_window = main_window
        self.DATA = database
        self.close_mfcc_event = threading.Event()  # Initialize the event

    def make_mfcc(self):
        """
                Scope:      1. get corresponding data and their details
                            2. Nomilize data
                            3. do pad if needed
                            4. make the mfcc through librosa library
                            5. call functions to save mfcc and  corresponding signal in .csv format
        """
        print('making mfcc.....wait')
        time_start = time.time()
        last_second_data = np.concatenate(self.DATA.last_second_c0)
        audio = last_second_data.astype(np.float32)
        frame_duration = 0.02
        sr = self.DATA.resp4.RESPEAKER_RATE
        frame_length = int(frame_duration * sr)
        normalized_frames = []

        # Normalize each frame by its maximum amplitude
        for i in range(0, len(audio), frame_length):
            frame = audio[i:i + frame_length]
            max_amp = np.max(np.abs(frame))
            normalized_frame = frame / max_amp if max_amp > 0 else frame
            normalized_frames.append(normalized_frame)

        normalized_audio = np.concatenate(normalized_frames)
        n_fft = 2048
        if len(normalized_audio) < n_fft:
            normalized_audio = np.pad(normalized_audio, (0, n_fft - len(normalized_audio)), mode='constant')

        mfcc = librosa.feature.mfcc(y=normalized_audio, sr=sr, n_mfcc=40, n_fft=2048, hop_length=512, fmax=8000)
        print("Done mfcc")
        """#self.main_window.axis_mfcc.clear()
        #librosa.display.specshow(mfcc, x_axis='time', ax=self.main_window.axis_mfcc)
        #self.main_window.axis_mfcc.set_ylabel('MFCC')
        #plt.figure(figsize=(10, 4))
        #librosa.display.specshow(mfcc, x_axis='time', sr=sr)
        #plt.colorbar(format='%+2.0f dB')
        #plt.title('MFCC')
        #plt.tight_layout()
        #plt.show()
        """

        # Create the directory based on the current time
        the_now_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        base_dir = os.getcwd()
        save_dir = os.path.join(base_dir, "MFCC_SIGNAL_saves", the_now_time)
        os.makedirs(save_dir, exist_ok=True)

        # Save the MFCC and signal to CSV
        self.DATA.Save_mfcc_csv(mfcc, save_dir)
        self.DATA.Save_signal_csv(normalized_audio, save_dir)


