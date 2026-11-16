import numpy as np
from scipy.fft import fft, fftfreq

def get_time_array(signal, sr):
    return np.linspace(0, len(signal) / sr, num=len(signal))

def compute_fft(signal, sr):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1 / sr)
    return xf[:N//2], 2.0/N * np.abs(yf[0:N//2])