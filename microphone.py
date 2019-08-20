import argparse
import os
import time
import wave
from datetime import datetime

import pyaudio

parser = argparse.ArgumentParser(description="Microphone")
parser.add_argument("--audio-dir", default="/speech/test_RT", help="where to save")
args = parser.parse_args()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10
# to stop the stream and restart every approx 200s
counter = 0
audio = pyaudio.PyAudio()
# where to save
rootdir = args.audio_dir + "/"
if not os.path.exists(rootdir):
    os.mkdir(rootdir)
while 1:
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime("%Y-%m-%d-t-%H-%M-%S")
    WAVE_OUTPUT_FILENAME = rootdir + str(st) + ".wav"

    # start Recording
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    print("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # stop Recording
    stream.stop_stream()
    # stream.close()
    # audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b"".join(frames))
    waveFile.close()
    counter += 1
    if counter == 20:
        counter = 0
        stream.close()
        audio.terminate()
        audio = pyaudio.PyAudio()
