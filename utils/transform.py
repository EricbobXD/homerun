import matplotlib.pyplot as plt
import numpy as np
from utils.save_file import save_photo

# waveform
def plot_waveform(rate, audio, title):
    time = np.linspace(0, len(audio) / rate, num = len(audio))
    #picture
    plt.figure(figsize=(12, 6)) #set picture size 12*6
    plt.plot(time, audio, label="Original") #import data into picture
    plt.title(f"{title} - Original") #set title 
    plt.xlabel("Time (s)") #set x-asis label
    plt.ylabel("Amplitude") #set y-asis label
    
    return save_photo()
#frequency_spectrum
def plot_frequency_spectrum(rate, audio, title):
    audio = audio.flatten() # audio change to one-dimensional array
    N = len(audio) 
    yf = np.fft.fft(audio) # audio by Fast Fourier Transform, it's a y-axis frequency
    xf = np.fft.fftfreq(N, 1 / rate)[:N // 2] #because audio is symmetry, it's can take half in x-asis

    plt.figure(figsize=(10, 4)) 
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    plt.title(f"{title} - Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid() #remove background

    return save_photo()