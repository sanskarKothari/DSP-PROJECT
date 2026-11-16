import numpy as np
from scipy import signal as scipy_signal

def add_white_gaussian_noise(clean_signal, snr_db):
    signal_power = np.mean(clean_signal ** 2)
    signal_power_db = 10 * np.log10(signal_power + 1e-10)
    noise_power_db = signal_power_db - snr_db
    noise_power = 10 ** (noise_power_db / 10)
    noise = np.random.normal(0, np.sqrt(noise_power), len(clean_signal))
    return clean_signal + noise

def apply_fir_filter(noisy_signal, sr, cutoff_freq, num_taps=101):
    nyquist = 0.5 * sr
    normalized_cutoff = cutoff_freq / nyquist
    h_n = scipy_signal.firwin(num_taps, normalized_cutoff, window='hamming')
    filtered_signal = scipy_signal.convolve(noisy_signal, h_n, mode='same')
    return filtered_signal, h_n

def apply_iir_filter(noisy_signal, sr, cutoff_freq, order=4):
    nyquist = 0.5 * sr
    normalized_cutoff = cutoff_freq / nyquist
    b, a = scipy_signal.butter(order, normalized_cutoff, btype='low')
    filtered_signal = scipy_signal.lfilter(b, a, noisy_signal)
    return filtered_signal, b, a

def check_iir_stability(a_coeffs):
    poles = np.roots(a_coeffs)
    magnitudes = np.abs(poles)
    is_stable = np.all(magnitudes < 1.0)
    return is_stable, poles, magnitudes