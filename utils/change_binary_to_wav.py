import wave
import os

def save_audio_data(audio_data, file_path):
    # 假設 audio_data 是加速後的音檔數據（例如 bytes）
    with open(file_path, "wb") as f:
        f.write(audio_data)

def get_sample_rate_from_audio(audio_data, rate):
    # 儲存加速後的音檔到臨時文件
    temp_file = "temp_accelerated_audio.wav"
    save_audio_data(audio_data, temp_file)
    
    # 讀取取樣率
    with wave.open(temp_file, 'rb') as wf:
        rate = wf.getframerate()  # 讀取取樣率
    
    # 刪除臨時檔案
    os.remove(temp_file)
    
    return rate
