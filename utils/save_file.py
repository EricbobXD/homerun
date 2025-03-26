import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import wave

def save_photo():
    file_name = f"waveform_{datetime.now().timestamp()}.png"
    file_path = os.path.join("static", file_name)
    plt.savefig(file_path)
    plt.close()
    print(file_name)
    return file_name

def save_audio(audio, rate, num_channels=1, sample_width=2):
    file_name = f"waveform_{datetime.now().timestamp()}.wav"
    file_path = os.path.join("static", file_name)

    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(num_channels)  # 設定聲道數量
        wf.setsampwidth(sample_width)  # 設定樣本寬度（例如 2 表示 16-bit）
        wf.setframerate(rate)          # 設定採樣率
        wf.writeframes(audio)          # 寫入音頻數據
    
    return file_name