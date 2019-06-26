import os
import re
import csv
import string
import pandas
import random

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from clean_text import clean_sentence



rootdir = "/speech/de_DE"


csv_output = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
         if(".csv" in file and file.startswith("metadata")):
            file_dir = os.path.join(subdir, file)
            #Too many csvs we are short on memory
            #os.system("mv "+file_dir +" /data/home/GPUAdmin1/asr/M-AILABS/csvs/" + file)
            with open(file_dir) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='|')
                for row in csv_reader:
                    print("filename: " + row[0])
                    print("transcript: " + row[2])
                    filename = row[0]
                    transcript = row[2]
                    transcript = clean_sentence(transcript)
                    wav_file_dir = "/speech/M-AILABS/"+ filename +".wav"
                    if(os.path.exists(wav_file_dir)):
                        csv_output.append((wav_file_dir, transcript))
                    
df = pandas.DataFrame(data=csv_output)
output_file = "/speech/M-AILABS/M-AILABS_all.csv"
df.to_csv(output_file, index=False, sep=",")
random.shuffle(csv_output)
csv_test = csv_output[0:5901]
csv_train = csv_output[5901:]        
df = pandas.DataFrame(data=csv_train)
output_file = "/data/home/GPUAdmin1/asr/train_csvs/M-AILABS_train.csv"
df.to_csv(output_file, index=False, sep=",")
df = pandas.DataFrame(data=csv_test)
output_file = "/data/home/GPUAdmin1/asr/test_csvs/M-AILABS_test.csv"
df.to_csv(output_file, index=False, sep=",")


#create dict from csvs
"""
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if(file.endswith(".wav")):
            file_dir = os.path.join(subdir, file)
            os.system("mv "+file_dir +" /data/home/GPUAdmin1/asr/M-AILABS/" + file)
"""