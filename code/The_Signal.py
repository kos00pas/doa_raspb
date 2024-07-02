import threading
import numpy as np
import pyaudio
import time

class Signal:
    def __init__(self, main_window, database):
        self.DATA = database
        self.main_window = main_window

        self.c0_stop_real_time_var = False
        self.p_recording = None
        self.stream_in = None
        self.stream_out = None
        self.c0_playback_thread = None
        self.stop_event = threading.Event()

    def start_recording(self):
        if not self.DATA.recording:
            self.DATA.recording = True
            print("Start rec, wait")
            self.DATA.time_of_Start = time.time()
            self.main_window.listening_button.config(state='normal')

            self.recording_thread = threading.Thread(target=self.record_audio)
            self.update_signal_thread = threading.Thread(target=self.update_signal_plot)
            self.recording_thread.start()
            self.update_signal_thread.start()

    def stop_recording(self):
        if self.DATA.recording:
            self.DATA.recording = False
            self.main_window.listening_button.config(state='disabled', text="Start Listen", bg="light yellow")
            self.main_window.make_mfcc_button.config(state='disabled', bg="light yellow")
            self.DATA.The_Saves_after_recording()
            self.stop_event.set()
            self.update_signal_thread.join(timeout=1)
            if self.update_signal_thread.is_alive():
                print("Warning: update_signal_thread did not terminate. Retrying...")
                self.update_signal_thread.join(timeout=3)
            self.c0_stop_real_time()

    def record_audio(self):
        self.p_recording = pyaudio.PyAudio()
        stream = self.p_recording.open(
            rate=self.DATA.resp4.RESPEAKER_RATE,
            channels=self.DATA.resp4.RESPEAKER_CHANNELS,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=self.DATA.resp4.RESPEAKER_INDEX,
            frames_per_buffer=self.DATA.resp4.CHUNK
        )
        self.stream_in = stream
        try:
            self.DATA.c0_buff = []
            self.DATA.last_second_c0 = []
            self.first_time = True
            self.DATA.frames = []
            while self.DATA.recording:
                data = stream.read(self.DATA.resp4.CHUNK, exception_on_overflow=False)
                self.DATA.frames.append(data)

                channel_data_chunk = np.frombuffer(data, dtype=np.int16)
                channel_data_chunk = channel_data_chunk.reshape(-1, self.DATA.resp4.RESPEAKER_CHANNELS).T
                c0 = channel_data_chunk[0]

                # for mfcc
                self.DATA.last_second_c0.append(c0)
                if len(self.DATA.last_second_c0) > self.DATA.chunks_per_second* self.DATA.second_rec_for_mfcc:
                    self.main_window.make_mfcc_button.config(state='normal', bg="cyan")
                    self.DATA.last_second_c0.pop(0)
                    
                
                #for signal  plotting 
                self.DATA.c0_buff.append(c0)
                if len(self.DATA.c0_buff) > self.DATA.seconds_signal_plotting * self.DATA.resp4.RESPEAKER_RATE / self.DATA.resp4.CHUNK:
                    self.DATA.c0_buff.pop(0)

        except Exception as e:
            print(f"An error occurred during recording: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            self.p_recording.terminate()
            print("Recording stopped")

    def update_signal_plot(self):
        if self.DATA.recording and len(self.DATA.c0_buff) > 0 and self.DATA.yes_plot_signal:
            audio_data = np.concatenate(self.DATA.c0_buff)
            time_in_seconds = np.arange(len(audio_data)) / self.DATA.resp4.RESPEAKER_RATE
            self.main_window.canvas.draw_idle()

        if self.DATA.recording and self.DATA.yes_plot_signal:
            self.main_window.after(self.DATA.signal_refresh, self.update_signal_plot)

    def c0_stop_real_time(self):
        self.c0_stop_real_time_var = False
        if self.c0_playback_thread is not None and self.c0_playback_thread.is_alive():
            self.c0_playback_thread.join(timeout=1)
            if self.c0_playback_thread.is_alive():
                print("Warning: c0_playback_thread did not terminate. Retrying...")
                self.c0_playback_thread.join(timeout=3)
        print("Stopped real-time playback.")

    def c0_play_real_time(self):
        if self.c0_playback_thread is None or not self.c0_playback_thread.is_alive():
            self.c0_playback_thread = threading.Thread(target=self.c0_play)
            self.c0_playback_thread.start()
        else:
            print("Playback thread is already running.")

    def c0_play(self):
        if not self.stream_in:
            print("Error: Input stream not open for playback")
            return

        self.c0_stop_real_time_var = True
        self.p_c0 = self.p_recording

        try:
            if not self.stream_out:
                self.stream_out = self.p_c0.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=self.DATA.resp4.RESPEAKER_RATE,
                    output=True,
                    output_device_index=2
                )

            print("Starting real-time playback. Press Escape, Backspace, or Space to stop.")

            while self.DATA.recording and self.c0_stop_real_time_var:
                data = self.stream_in.read(self.DATA.resp4.CHUNK, exception_on_overflow=False)
                np_data = np.frombuffer(data, dtype=np.int16)
                channel_data = np_data.reshape(-1, self.DATA.resp4.RESPEAKER_CHANNELS)[:, 0]
                mono_data = channel_data.tobytes()
                self.stream_out.write(mono_data)

        except Exception as e:
            print(f"An error occurred during real-time playback: {e}")
        finally:
            try:
                if self.stream_out:
                    self.stream_out.stop_stream()
                    self.stream_out.close()
                    self.stream_out = None
            except Exception as e:
                print(f"Error closing streams: {e}")
            print("Real-time playback and recording stopped.")

    def for_destroy(self):
        self.stop_event.set()
        if hasattr(self, 'DATA'):
            self.DATA.recording = False

        if self.stream_in is not None:
            try:
                self.stream_in.stop_stream()
                self.stream_in.close()
            except Exception as e:
                print(f"Error closing input stream: {e}")
            self.stream_in = None

        if self.stream_out is not None:
            try:
                self.stream_out.stop_stream()
                self.stream_out.close()
            except Exception as e:
                print(f"Error closing output stream: {e}")
            self.stream_out = None

        if self.p_recording is not None:
            self.p_recording.terminate()

        if self.c0_playback_thread is not None and self.c0_playback_thread.is_alive():
            self.c0_playback_thread.join(timeout=1)
            if self.c0_playback_thread.is_alive():
                print("Warning: c0_playback_thread did not terminate. Retrying...")
                self.c0_playback_thread.join(timeout=3)

        self.p_recording = None
        self.c0_playback_thread = None
