import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import io

from src.sedsp.audio_io import load_audio
from src.sedsp.analysis import get_time_array, compute_fft
from src.sedsp.filters import add_white_gaussian_noise, apply_fir_filter, apply_iir_filter, check_iir_stability

st.set_page_config(page_title="DSP Speech Enhancement", layout="wide")
st.title("Speech Enhancement using Digital Signal Processing")

st.sidebar.header("1. Upload Audio")
uploaded_file = st.sidebar.file_uploader("Upload a WAV file", type=["wav"])

if uploaded_file is not None:
    clean_signal, sr = load_audio(uploaded_file)
    st.sidebar.success(f"Loaded! Sampling Rate: {sr} Hz")
    
    st.sidebar.header("2. Noise Injection")
    snr_db = st.sidebar.slider("Signal-to-Noise Ratio (dB)", -10, 30, 5)
    noisy_signal = add_white_gaussian_noise(clean_signal, snr_db)
    
    st.sidebar.header("3. Filter Design")
    filter_type = st.sidebar.radio("Select Filter Type", ["FIR (Window Method)", "IIR (Butterworth)"])
    cutoff = st.sidebar.slider("Cutoff Frequency (Hz)", 500, int(sr/2)-100, 3000)
    
    if filter_type == "FIR (Window Method)":
        num_taps = st.sidebar.slider("Number of Taps (N)", 11, 201, 101, step=2)
        filtered_signal, coeffs = apply_fir_filter(noisy_signal, sr, cutoff, num_taps)
        st.sidebar.info("FIR filters are always stable (all poles at origin).")
    else:
        order = st.sidebar.slider("Filter Order", 2, 10, 4)
        filtered_signal, b, a = apply_iir_filter(noisy_signal, sr, cutoff, order)
        is_stable, poles, mags = check_iir_stability(a)
        if is_stable:
            st.sidebar.success(f"System is STABLE (Max pole magnitude: {np.max(mags):.4f} < 1)")
        else:
            st.sidebar.error("System is UNSTABLE (Poles outside unit circle!)")

    col1, col2, col3 = st.columns(3)
    
    def create_audio_bytes(sig, rate):
        buf = io.BytesIO()
        sf.write(buf, sig, rate, format='WAV')
        return buf.getvalue()

    with col1:
        st.subheader("Original Speech")
        st.audio(create_audio_bytes(clean_signal, sr), format="audio/wav")
    with col2:
        st.subheader(f"Noisy Speech (SNR: {snr_db}dB)")
        st.audio(create_audio_bytes(noisy_signal, sr), format="audio/wav")
    with col3:
        st.subheader(f"Enhanced ({filter_type.split()[0]})")
        st.audio(create_audio_bytes(filtered_signal, sr), format="audio/wav")

    st.divider()

    st.header("Time-Domain & Frequency-Domain Analysis")
    
    time_arr = get_time_array(clean_signal, sr)
    xf_clean, yf_clean = compute_fft(clean_signal, sr)
    xf_noisy, yf_noisy = compute_fft(noisy_signal, sr)
    xf_filt, yf_filt = compute_fft(filtered_signal, sr)

    fig, axs = plt.subplots(3, 2, figsize=(15, 10))
    fig.tight_layout(pad=4.0)

    axs[0, 0].plot(time_arr, clean_signal, color='blue', alpha=0.7)
    axs[0, 0].set_title("Clean Signal (Time Domain)")
    axs[0, 0].set_ylabel("Amplitude")

    axs[1, 0].plot(time_arr, noisy_signal, color='red', alpha=0.7)
    axs[1, 0].set_title("Noisy Signal (Time Domain)")
    axs[1, 0].set_ylabel("Amplitude")

    axs[2, 0].plot(time_arr, filtered_signal, color='green', alpha=0.7)
    axs[2, 0].set_title("Filtered Signal (Time Domain)")
    axs[2, 0].set_ylabel("Amplitude")
    axs[2, 0].set_xlabel("Time (s)")

    axs[0, 1].plot(xf_clean, yf_clean, color='blue')
    axs[0, 1].set_title("Clean Signal Spectrum")
    axs[0, 1].set_xlim(0, 5000)

    axs[1, 1].plot(xf_noisy, yf_noisy, color='red')
    axs[1, 1].set_title("Noisy Signal Spectrum")
    axs[1, 1].set_xlim(0, 5000)

    axs[2, 1].plot(xf_filt, yf_filt, color='green')
    axs[2, 1].set_title("Filtered Signal Spectrum")
    axs[2, 1].set_xlim(0, 5000)
    axs[2, 1].set_xlabel("Frequency (Hz)")

    st.pyplot(fig)
else:
    st.info("Please upload a .wav file in the sidebar to begin processing.")