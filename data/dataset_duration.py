import os
import csv
import wave
import datetime
from pydub import AudioSegment

time = datetime.timedelta(milliseconds=0)
root = "/home/GPUAdmin1/asr/"
csv_folders = ["test_csvs", "dev_csvs", "train_csvs"]
for csv_folder in csv_folders:
    for file_dir in os.listdir(root + csv_folder):
        with open(root + csv_folder + "/" + file_dir, encoding="utf-8-sig") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader, None)
            for row in csv_reader:
                wav_dir = row[0]
                millis = len(AudioSegment.from_wav(wav_dir))
                time += datetime.timedelta(milliseconds=millis)
                print(wav_dir, end="\r")
        print("ended " + file_dir)
        print(time.seconds / 3600 + time.days * 24)
        print("*******")
        time = datetime.timedelta(milliseconds=0)