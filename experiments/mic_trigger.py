# mic_trigger.py

import sounddevice as sd
import numpy as np

# Record 3 seconds of audio
fs = 44100  # Sample rate
duration = 3  # seconds
print("Recording...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
print("Recording complete!")