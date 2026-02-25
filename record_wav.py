import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

def get_audio_input():
    # sampling frequency
    freq = 44100

    # recording duration
    duration = 5

    # start recorder with the given values 
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=2)
    print("Recording Audio...")

    # record audio for the given number of seconds
    sd.wait()
    print("Audio recorded.")

    # convert NumPy array to audio file
    wv.write("recording1.wav", recording, freq, sampwidth=2)
