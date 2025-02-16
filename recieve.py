import pyaudio
import fft_utils
import numpy
import struct
import sys
CHUNK = 16384
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = CHUNK * 2
FFT_SIZE = 2**13
BD = 255
RECORD_SECONDS = int(sys.argv[1])

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")
f = open("test.bin","wb")
def convert_buffer(buf, max_items):
    buf = buf[:max_items*2]
    return struct.unpack("%dh" % max_items, buf)
def compute_freq(sample):
    return float(sample)*2*RATE/FFT_SIZE
def recognize_note(audio_data):
    """return the note played in the given audio data
    Params:
        audio_data - a buffer of samples
    Return value:
        The frequency of the playing note. 
        If no playing note is found, None is returned.
    """
    mult = fft_utils.awindow(len(audio_data))
    print(mult)
    print(FFT_SIZE/12)
    final_fft = numpy.array(list(map(abs, numpy.fft.fft(audio_data*mult)[:round(FFT_SIZE/12)])))
    
    signature = [peak for peak in fft_utils.find_peaks(final_fft,2) if peak[0]>10]
        
    if len(signature) == 0:
        return
            
    note = min([x[0] for x in signature])
    return compute_freq(note)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-=_+[]\\{}|<>?/.,`~!@#$%^&*) "
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    avg = 0
    #print(data[0])
    ld = 0
    navg = 1
    navq = 1
    wrt = False
    to_fft = convert_buffer(data,FFT_SIZE)
    stepone = recognize_note(to_fft)/2
    print("stepone")
    print(stepone)
    print("Eval0")
    stepone -= 10
    print("Eval1")
    eval1 = round(stepone/10)
    print(eval1)
    evaluated = eval1
    print("post-evaluation")
    #if evaluated > 199:
    #    evaluated -= 100
    #while not chr(evaluated) in alphabet:
    #    print(" SHIFT DOWN")
    #    evaluated -= 24
    #    if evaluated < 0:
    #        evaluated = 0x20
    print(evaluated)
    #print(round(recognize_note(to_fft)/10) - 10)
    f.write(evaluated.to_bytes())
    #print(round(avg/10) - 10)
    #f.write(round((round(avg))/10 - 10).to_bytes())
    #f.write(data[0].to_bytes())
f.close()