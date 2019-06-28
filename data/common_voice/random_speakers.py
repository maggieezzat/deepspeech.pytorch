import os
import csv
import wave
import datetime
from pydub import AudioSegment

time = datetime.timedelta(milliseconds=0)
root = "/speech/common_voice_de/common_voice_valid_wav.csv"
speakers = []
test = []
hours_so_far = 0
hours_needed = 7
speaker = ""
with open(root, encoding="utf-8-sig") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        wav_dir = row[0]
        speaker = wav_dir.split("spk",1)[1].split("_",1)[0]
        speakers.append(speaker)
        millis = len(AudioSegment.from_wav(wav_dir))
        time += datetime.timedelta(milliseconds=millis)
        hours_so_far += time.seconds/3600 +  time.days * 24
        if hours_so_far >= hours_needed:
            break
        print(hours_so_far, end="\r")

print()
print(len(set(speakers)))
print(speakers[-1])
print("*******")

