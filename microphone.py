import wave
import time
import pyaudio
from datetime import datetime

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10
#to stop the stream and restart every approx 200s
counter = 0
#where to save
rootdir = "E:/trial/"
while 1:
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d-t-%H-%M-%S')
    WAVE_OUTPUT_FILENAME = rootdir+str(st)+".wav"
 
    audio = pyaudio.PyAudio()
 
# start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("finished recording")
 
 
# stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    counter +=1
    if(counter ==20):
        counter =0
        stream.close()
        audio.terminate()
        audio = pyaudio.PyAudio()
