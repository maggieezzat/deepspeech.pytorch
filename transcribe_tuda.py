import os
import csv
import time
#given that the worker and server are already running

with open("home/GPUAdmin1/asr/test.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        os.system("./home/GPUAdmin1/kaldi/egs/tuda/decode_wav.sh"+ " "+ row[0])
        #give the server some time
        time.sleep(0.25)