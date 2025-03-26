# extract watermark
def extract_watermark(audio, watermark_length=32):
    audio = audio.flatten()
    # LSB
    watermark_bits = ''.join(str(audio[i] & 1) for i in range(watermark_length))
    encryption_id = ''.join(hex(int(watermark_bits[i:i + 4], 2))[2:].upper() for i in range(0, len(watermark_bits), 4))
    return encryption_id

# remove watermark
def remove_watermark(audio, watermark_length=32):
    audio = audio.copy().flatten()
    for i in range(watermark_length):
        audio[i] = audio[i] & ~1
    return audio