import os
import csv
import wave
import datetime
from pydub import AudioSegment

time = datetime.timedelta(milliseconds=0)
root = "/speech/common_voice_de/common_voice_valid_wav.csv"
speakers = []
test = []
dev = []
train = []
hours_so_far = 0
hours_needed = 7
speaker = ""
dataset = 0
with open(root, encoding="utf-8-sig") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        wav_dir = row[0]
        speaker = wav_dir.split("spk", 1)[1].split("_", 1)[0]
        speakers.append(speaker)
        millis = len(AudioSegment.from_wav(wav_dir))
        time += datetime.timedelta(milliseconds=millis)
        hours_so_far += time.seconds / 3600 + time.days * 24
        if dataset == 0:
            test.append(row)
        elif dataset == 1:
            dev.append(row)
        else:
            train.append(row)
        if hours_so_far >= hours_needed or csv_reader[-1] is row:
            print()
            print(dataset)
            print()
            dataset += 1
            print(hours_so_far)
            hours_so_far = 0
            if dataset == 1:
                hours_needed = 26
            else:
                hours_needed = 320

print()
print(len(test))
print(len(dev))
print(len(train))
print("*******")

