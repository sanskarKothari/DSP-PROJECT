import soundfile as sf
import numpy as np

def load_audio(file_path):
    signal, sr = sf.read(file_path)
    if len(signal.shape) > 1:
        signal = np.mean(signal, axis=1) # Convert stereo to mono
    return signal, sr

def save_audio(file_path, signal, sr):
    sf.write(file_path, signal, sr)