import os
import csv
import wave
import datetime
from pydub import AudioSegment
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--hours", type=int, default=7)
args = parser.parse_args()

time = datetime.timedelta(milliseconds=0)
root = "/home/GPUAdmin1/asr/common_voice_all_valid_utt.csv"
speakers = []
test = []
hours_so_far = 0
hours_needed = args.hours
speaker = ""
with open(root, encoding="utf-8-sig") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        wav_dir = row[0]
        speaker = wav_dir.split("spk", 1)[1].split("_", 1)[0]
        speakers.append(speaker)
        millis = len(AudioSegment.from_wav(wav_dir))
        time = datetime.timedelta(milliseconds=millis)
        hours_so_far += time.seconds / 3600 + time.days * 24
        print(hours_so_far, end="\r")
        if hours_so_far >= hours_needed:
            break

print()
print(len((speakers)))
print(speakers[-1])
print("*******")
