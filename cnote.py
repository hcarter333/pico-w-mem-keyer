import numpy as np
import wave
import base64

# Parameters for the audio
sample_rate = 44100  # Samples per second
duration = 5  # seconds
frequency = 261.63  # Frequency of middle C in Hz

# Generate the time points
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate the audio wave (sine wave for a pure tone)
audio_wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # 0.5 for volume control

# Convert to 16-bit PCM format
audio_wave = np.int16(audio_wave * 32767)  # Scale to int16 range

# Save to a WAV file
wav_file_path = 'middle_c_5_seconds.wav'
with wave.open(wav_file_path, 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16 bits
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(audio_wave.tobytes())

# Read the WAV file and encode it in base64
with open(wav_file_path, 'rb') as audio_file:
    audio_data = audio_file.read()
    base64_audio = base64.b64encode(audio_data).decode('utf-8')

base64_audio  # Output the complete base64 string for the audio
