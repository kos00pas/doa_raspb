import os
import sys
import threading
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import The_Classification_Window, The_DOA_resp, The_Parameters_Window
import The_Signal


##########################################################
class Main_Window(tk.Tk):
    def __init__(self, gui_manager, database):
        super().__init__()
        self.close_mfcc_event = threading.Event()
        '''
            Scope       : GUI main window plot 
            Task of Fun : 1. initialize window ->  self.main_window_init()
                          2. initialize doa     -> The_DOA_resp
        '''
        self.DATA = database
        (self.mfcc_thread, self.canvas, self.doa_thread, self.apppend_parameters_button, self.doaa_2d_label,
         self.doa_save_button, self.doaa_label,
         self.saved_to_label, self.c4_stop_last_data_button, self.saving_button,
         self.c4_play_last_data_button, self.c0_stop_last_data_button, self.c0_play_last_data_button,
         self.signal_label, self.control_frame, self.canvas1, self.canvas2,
         self.axis_signal, self.axis_mfcc, self.axis_doa_resp, self.axis_tdoa_2d, self.axis_tdoa3d, self.fig,
         self.parameters_button,
         self.up_control_frame, self.the_signal,
         self.classification_button, self.stop_button, self.start_button,
         self.down_control_frame) = (None,) * 30
        self.main_window_init()
        self.doa_plot = The_DOA_resp.The_DOA_resp(self.DATA, self)

    def main_window_init(self):
        '''
                    Scope       : 1. Initialize control frame -> buttons around the window's perimeter
                                  3. Signal initialization
                                  2. Parameter window init.   -> connections with device( ReSpeaker mic array v2) and
                                                              -> set the buttons based on ReSpeaker
        '''
        #check operating system
        if sys.platform.startswith('win'):
            self.state('zoomed')
        else:  # For Linux and other systems
            self.attributes('-zoomed', True)
        self.title("Localization Window")
        self.fig = plt.figure(figsize=(12, 10))  # Create a larger figure for better layout management

        # when the window close
        self.protocol("WM_DELETE_WINDOW", self.on_close_main_window)

        self.setup_control_frames()
        # Initialize the RecordingControls
        self.the_signal = The_Signal.Signal(self, self.DATA)
        # Initialize the parameter space window with the new control frame
        self.parameter_space = The_Parameters_Window.Parameters_Window(self.DATA, self.control_frame)

        # Configure the grid to take full space
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)
        '''##gs = gridspec.GridSpec(1, 1)

        # Adjust the plot areas
        ##self.axis_doa_resp = self.fig.add_subplot(gs[0], polar=True)
        #self.axis_signal = self.fig.add_subplot(gs[1])
        #self.axis_mfcc = self.fig.add_subplot(gs[2])

        ##self.axis_doa_resp.set_title('ReSpeaker')
        ##self.axis_doa_resp.xaxis.set_ticks([])
        ##self.axis_doa_resp.yaxis.set_ticks([])

        ##self.fig.tight_layout(pad=3)

        # Embed the figure in a Tkinter canvas
        ###self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        ##self.canvas.draw()
        ##self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=4, sticky='nsew')  # Span over 4 rows for better adjustment
        '''

    def setup_control_frames(self):
        """
                    Scope : buttons around the window's perimeter
        """

        """Bottom Control frame for Buttons"""
        self.down_control_frame = tk.Frame(self)
        self.down_control_frame.grid(row=4, column=0, columnspan=2, sticky='ew')

        """1. Recording """
        self.rec_button = tk.Button(self.down_control_frame, text="Start Recording", command=self.toggle_recording,
                                    bg="light yellow", state='normal')
        self.rec_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.saving_button = tk.Button(self.down_control_frame, text="saving recording?",
                                       command=lambda: self.change_state_red_green(self.saving_button,
                                                                                   "save_recording_enable"))
        self.saving_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.initial_color(self.saving_button, "save_recording_enable")

        """2. Print recording time"""
        self.signal_label = tk.Label(self.down_control_frame, text="Sec:", width=20)
        self.signal_label.pack(side=tk.LEFT, padx=5, pady=5)
        """Real time playback -> need fixing """
        self.DATA.listening = False
        self.listening_button = tk.Button(self.down_control_frame, text="Start Listen", command=self.toggle_listen,
                                          bg="light yellow", state='disabled')
        self.listening_button.pack(side=tk.LEFT, padx=5, pady=5)

        """3. MFCC"""
        self.make_mfcc_button = tk.Button(self.down_control_frame, text="Mfcc", command=self.make_mfcc,
                                          state='disabled')
        self.make_mfcc_button.pack(side=tk.RIGHT, padx=5, pady=5)
        """4. appent parameters """
        self.apppend_parameters_button = tk.Button(self.down_control_frame, text="Append Parameters",
                                                   command=self.DATA.append_parameters)
        self.apppend_parameters_button.pack(side=tk.RIGHT, padx=5, pady=5)
        """5. DOA"""
        self.doaa_label = tk.Label(self.down_control_frame, text="DOA: ", width=20, font="bold")
        self.doaa_label.pack(side=tk.RIGHT, padx=5, pady=5)
        """6. Print saved directory """
        self.saved_to_label = tk.Label(self.down_control_frame, text="Save:", width=20)
        self.saved_to_label.pack(side=tk.RIGHT, padx=5, pady=5)

        # Directly use the main window for controls without inner_frame
        self.control_frame = tk.Frame(self, bg="white", bd=1.4, relief="solid")
        self.control_frame.grid(row=0, column=0, rowspan=4, sticky='nsew', padx=10,
                                pady=(50, 10))  # Add top padding , padx=10, pady=(50, 10))

        # Create a label for the control frame title
        self.control_frame_title = tk.Label(self.control_frame, text="\t\t\t\t", bg="white", font=("Arial", 15))
        self.control_frame_title.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

    def toggle_listen(self):
        if self.DATA.listening:
            self.the_signal.c0_stop_real_time()
            self.listening_button.config(text="Start Listen ", bg="cyan")
        else:
            self.the_signal.c0_play_real_time()
            self.listening_button.config(text="Stop  Listen", bg="magenta")
        self.DATA.listening = not self.DATA.listening

    def toggle_recording(self):
        if self.DATA.recording:
            self.the_signal.stop_recording()
            self.rec_button.config(text="Start recording", bg="light yellow")
        else:
            self.the_signal.start_recording()
            self.rec_button.config(text="Stop  recording", bg="magenta")
        # self.DATA.recording = not self.DATA.recording

    def make_mfcc(self):
        """
                Scope:      When the button of Mfcc pressed then run that function
        """

        def thread_mfcc_function():
            classf = The_Classification_Window.Classification_Window(self, self.DATA)
            classf.make_mfcc()

        self.mfcc_thread = threading.Thread(target=thread_mfcc_function)
        self.mfcc_thread.start()
        self.mfcc_thread.join()

    def on_close_main_window(self):
        """
                Scope:      Destroy threads appropriate in order to close application
        """
        print("**Wait for closing")

        def delayed_exit():
            import time
            time.sleep(1)  # Wait a bit for cleanup to complete
            try:
                sys.exit(0)
            except:
                print("Oh")
                os._exit(0)

        """Handle the window close event."""
        self.DATA.save_doa_param_folder()
        if self.mfcc_thread is not None and self.mfcc_thread.is_alive():
            self.close_mfcc_event.set()  # Signal the thread to close
            self.mfcc_thread.join()
        self.the_signal.stop_recording()
        self.the_signal.for_destroy()
        self.doa_plot.for_destroy()
        self.quit()
        self.destroy()  # Destroy the main window
        threading.Thread(target=delayed_exit).start()

    def initial_color(self, button, attribute_name):
        """
            Scope :  Access the attribute's initial state and set the corresponding color to the button
        """
        state = getattr(self.DATA, attribute_name)

        if state:
            button.config(bg='green')
        else:
            button.config(bg='red')

    def change_state_red_green(self, button, attribute_name):
        """
            Scope :  Access the attribute's current state and set the corresponding color to the button
        """
        current_state = getattr(self.DATA, attribute_name)
        new_state = not current_state
        setattr(self.DATA, attribute_name, new_state)

        if new_state:
            button.config(bg='green')
            print("Enable Saving ", attribute_name)
        else:
            button.config(bg='red')
            print("Disable Saving  ", attribute_name)
