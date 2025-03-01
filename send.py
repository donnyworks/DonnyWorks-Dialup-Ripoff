import pyaudio
from math import pi
import numpy as np
import sys
from scipy import signal
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=16000, output=1,)
#length = float(sys.argv[2])
if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " [filename] [OPTIONAL: baud rate (default is two)]")
    exit()
if len(sys.argv) > 2:
    length = 1/int(sys.argv[2])
else:
    length = 0.5
f = open(sys.argv[1],"rb").read()

def make_sinewave(frequency, length, sample_rate=44100):
    length = int(length * sample_rate)
    factor = float(frequency) * (pi * 2) / sample_rate
    waveform = np.sin(np.arange(length) * factor)

    return waveform
def make_squarewave(frequency,length, sample_rate=44100):
    length = int(length * sample_rate)
    t = np.linspace(0, 2)
    waveform = signal.square(2*pi*frequency*t)
    return waveform
for i in f:
    print("Initial value")
    print(i)
    print("Output frequency:")
    print(i*10 + 10)
    wave = make_sinewave((i*10) + 10, length, 16000)
    a = wave.astype(np.float32).tobytes()
    stream.write(a)
stream.stop_stream()
stream.close()