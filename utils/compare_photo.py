import io
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from utils.save_file import save_photo

# Plot waveform from binary audio data
def plot_waveform_compare(audio1, rate1, audio2, rate2, title):
    print(1)
    time1 = np.linspace(0, len(audio1) / rate1, num = len(audio1))
    time2 = np.linspace(0, len(audio2) / rate2, num = len(audio2))
    
    #picture
    plt.figure(figsize=(12, 6)) #set picture size 12*6

    plt.subplot(2, 1, 1)
    plt.plot(time1, audio1, label="Original") #import data into picture
    plt.title(f"{title} - Original") #set title 
    plt.xlabel("Time (s)") #set x-asis label
    plt.ylabel("Amplitude") #set y-asis label

    plt.subplot(2, 1, 2)
    plt.plot(time2, audio2, label="Original") #import data into picture
    plt.xlabel("Time (s)") #set x-asis label
    plt.ylabel("Amplitude") #set y-asis label

    plt.tight_layout()
    return save_photo()

# Plot spectrogram from binary audio data
def plot_spectrogram_compare(audio1, rate1, audio2, rate2, title):
    audio1 = audio1.astype(np.float32) / np.max(np.abs(audio1))  # 假設 audio1 是 int16 型別
    audio2 = audio2.astype(np.float32) / np.max(np.abs(audio2))  # 假設 audio2 是 int16 型別
    
    # 計算第一個音頻的頻譜圖
    D1 = np.abs(librosa.stft(audio1))  # 計算 STFT 並取絕對值
    D2 = np.abs(librosa.stft(audio2))  # 計算 STFT 並取絕對值

    # 將頻譜圖轉換為 dB（對數尺度）
    D1_db = librosa.amplitude_to_db(D1, ref=np.max)  # 轉換為 dB
    D2_db = librosa.amplitude_to_db(D2, ref=np.max)  # 轉換為 dB

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.imshow(D1_db, aspect='auto', origin='lower', cmap='inferno', 
               extent=[0, len(audio1) / rate1, 0, rate1 / 2])
    plt.title(f"{title} - Audio 1 Spectrogram")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(format='%+2.0f dB')

    plt.subplot(2, 1, 2)
    plt.imshow(D2_db, aspect='auto', origin='lower', cmap='inferno', 
               extent=[0, len(audio2) / rate2, 0, rate2 / 2])
    plt.title(f"{title} - Audio 2 Spectrogram")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(format='%+2.0f dB')

    plt.tight_layout()
    return save_photo()