from pydub import AudioSegment
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64
import io

# 生成 AES 金鑰
def generate_key():
    return os.urandom(16)  # 128位的 AES 金鑰

# 加密音訊
def encrypt_audio(input_audio_path, key):
    try:
        # 讀取音訊檔案
        audio = AudioSegment.from_file(input_audio_path)
    except Exception as e:
        raise ValueError(f"無法讀取音訊檔案: {e}")

    # 將音訊數據轉換為位元組
    audio_bytes = io.BytesIO()
    audio.export(audio_bytes, format="wav")
    audio_data = audio_bytes.getvalue()
    
    # 使用AES進行加密
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(audio_data) + padder.finalize()

    iv = os.urandom(16)  # 初始向量
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # 加密後的音訊數據保存為檔案
    encrypted_audio_path = input_audio_path + ".enc"
    with open(encrypted_audio_path, "wb") as f:
        f.write(iv + encrypted_data)  # iv + 加密數據一起儲存

    return encrypted_audio_path, base64.b64encode(key).decode('utf-8')

# 解密音訊
def decrypt_audio(input_encrypted_audio_path, key):
    try:
        # 讀取加密的音訊檔案
        with open(input_encrypted_audio_path, "rb") as f:
            encrypted_data = f.read()
    except Exception as e:
        raise ValueError(f"無法讀取加密檔案: {e}")

    iv = encrypted_data[:16]  # 提取iv
    encrypted_audio_data = encrypted_data[16:]  # 剩餘的加密數據

    # 使用AES進行解密
    cipher = Cipher(algorithms.AES(base64.b64decode(key)), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_audio_data) + decryptor.finalize()

    # 去掉填充
    unpadder = padding.PKCS7(128).unpadder()
    original_data = unpadder.update(decrypted_data) + unpadder.finalize()

    # 將解密的音訊數據轉換為音訊檔案
    output_audio_path = input_encrypted_audio_path.replace(".enc", ".dec.wav")
    with open(output_audio_path, "wb") as f:
        f.write(original_data)

    return output_audio_path

# 測試加解密流程
if __name__ == "__main__":
    input_audio_path = "C:/Users/user/Downloads/a.wav"  # 輸入音訊檔案路徑
    
    # 生成加密金鑰
    key = generate_key()

    # 加密音訊
    encrypted_audio_path, key_base64 = encrypt_audio(input_audio_path, key)
    print(f"加密完成，金鑰: {key_base64}")

    # 假設我們有金鑰，現在解密
    decrypted_audio_path = decrypt_audio(encrypted_audio_path, key_base64)
    print(f"解密完成，解密後的音訊路徑: {decrypted_audio_path}")