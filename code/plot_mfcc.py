import os
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

def load_mfcc_from_csv(file_path):
    # Load the MFCC data from the CSV file
    mfcc = np.loadtxt(file_path, delimiter=',')
    return mfcc

def process_all_mfcc_files(base_dir):
    mfcc_list = []
    # Traverse all subdirectories to find mfcc.csv files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == 'mfcc.csv':
                file_path = os.path.join(root, file)
                print(f'Processing file: {file_path}')
                mfcc = load_mfcc_from_csv(file_path)
                mfcc_list.append(mfcc)
    return mfcc_list

def plot_combined_mfcc(mfcc_list, sr=16000):
    num_mfcc = len(mfcc_list)
    fig, axs = plt.subplots(num_mfcc, 1, figsize=(10, 4 * num_mfcc))
    
    if num_mfcc == 1:
        axs = [axs]  # Ensure axs is iterable even if there's only one plot
    
    for i, mfcc in enumerate(mfcc_list):
        img = librosa.display.specshow(mfcc, x_axis='time', sr=sr, ax=axs[i])
        axs[i].set_title(f'MFCC {i + 1}')
        fig.colorbar(img, ax=axs[i], format='%+2.0f dB')
    
    plt.tight_layout()
    plt.show()

# Set the base directory to the current working directory
base_dir = os.getcwd()

# Process all mfcc.csv files in the subdirectories
mfcc_list = process_all_mfcc_files(base_dir)

# Plot all MFCCs together in separate subplots
plot_combined_mfcc(mfcc_list)
