# Speech Enhancement Using Digital Signal Processing Techniques

## Objective

To analyse and enhance speech signals using digital signal processing (DSP) techniques by studying their time-domain and frequency-domain characteristics, introducing noise, and designing suitable FIR and IIR digital filters for noise reduction. This project demonstrates practical applications of sampling and reconstruction, convolution, Fourier transform, Z-transform, system stability, and digital filter implementation.

## Features

- **Audio Processing**: Sampling and reconstruction of `.wav` files.
- **Noise Injection**: Additive White Gaussian Noise (AWGN) with adjustable Signal-to-Noise Ratio (SNR).
- **Filter Design**:
  - FIR filter design using the Window method (Hamming).
  - IIR filter design (Butterworth) with adjustable order.
- **System Stability Check**: Calculates Z-transform poles to verify IIR system stability.
- **DSP Visualization**: Interactive plots for Time-Domain amplitude and Frequency-Domain spectra (Fast Fourier Transform).

## Project Structure

```text
speech_enhancement_dsp/
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── data/                       # Directory for sample .wav files
└── src/
    └── sedsp/                  # Core DSP Python package
        ├── __init__.py
        ├── audio_io.py         # Audio loading, saving, and sampling
        ├── analysis.py         # Time and frequency domain analysis (FFT)
        └── filters.py          # FIR/IIR design, convolution, and Z-transform stability
```
