import random
from scipy.signal import resample
import numpy as np
# generate random hex string 
def generate_random_hex_string():
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(8))

# bytes xor to hex string
def bytes_xor_to_hexstring(ba1, ba2):
    return bytes([a ^ b for a, b in zip(ba1, ba2)]).hex()

# generate encryption id
def generate_encryption_id():
    A1 = generate_random_hex_string()
    A2 = generate_random_hex_string()
    B1 = generate_random_hex_string()
    B2 = generate_random_hex_string()
    ba_xor_A = bytes_xor_to_hexstring(bytes.fromhex(A1), bytes.fromhex(A2))
    ba_xor_B = bytes_xor_to_hexstring(bytes.fromhex(B1), bytes.fromhex(B2))
    final_id = bytes_xor_to_hexstring(bytes.fromhex(ba_xor_A), bytes.fromhex(ba_xor_B)).upper()
    print(f"浮水印密鑰，請妥善保存: {final_id}")
    return final_id

# embed watermark
def embed_watermark(audio, encryption_id):
    watermark_bits = ''.join(format(int(char, 16), '04b') for char in encryption_id) # converts each hexadecimal character into a 4-bit binary represent ation and concatenates all the binary strings
    audio = audio.flatten() # from multi-dimensional to one dimensional

    # LSB
    for i, bit in enumerate(watermark_bits):
        audio[i] = (audio[i] & ~1) | int(bit)
    return audio

# speed up audio
def speed_up_audio(audio, speed_factor=2.0):
    num_samples = int(len(audio) / speed_factor)
    resampled_audio = resample(audio, num_samples) # resampling the audio
    # clips the resampled audio values to fit within the range of 16-bit signed integers, which is the typical range for audio samples.
    resampled_audio = np.clip(resampled_audio, -32768, 32767).astype(np.int16)

    return resampled_audio