import os
from pydub import AudioSegment
import re
import csv
import string
import pandas
import random
from os import listdir, remove
from os.path import isfile, join
import soundfile

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from clean_text import clean_sentence


dir = "/speech/spoken_wikipedia_german/"




def convert_to_wav():
    
    SWC_path = "/speech/SWC_wav/"

    if not os.path.exists(SWC_path):
        os.makedirs(SWC_path)
    
    with open("wav.txt") as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]
    for line in lines:
        os.system(line[16:-3] + SWC_path + line[0:15] + ".wav")





def segment_wav():

    data_dir = "/speech/SWC_wav/"

    segmented_files_dir = "/speech/spoken_wikipedia_german/"
    if not os.path.exists(segmented_files_dir):
        os.makedirs(segmented_files_dir)
    
    with open("segments.txt", 'r') as f:
        lines = f.readlines()

    total = len(lines)

    lines = [l.strip() for l in lines]

    #i=0
    for line in lines:
        #i+=1
        #if i < 60000:
        #    print("Skipping " + str(i), end='\r')
        #    continue
        line = line.split(' ')
        old_file = os.path.join(data_dir, line[1])
        new_file = os.path.join(segmented_files_dir, line[0])
        t1 = float(line[2]) * 1000
        t2 = float(line[3]) * 1000

        newAudio = AudioSegment.from_wav( old_file +".wav")
        newAudio = newAudio[t1:t2]
        newAudio.export(new_file + '.wav', format="wav")
        
        print(str(i) + " / " + str(total) , end='\r')




def gen_corrupted_list_swc(root_dir=dir):
    
    corrupted_files = []

    files = [
            f
            for f in listdir(root_dir)
            if isfile(join(root_dir, f))
        ]

    total_files=len(files)
    processed_files = 0
    
    for file in files:
        processed_files+=1
        if ".wav" in file: 
            print("Checking files: " + str(processed_files) + "/" + str(total_files), end="\r")
            if os.path.getsize(join(root_dir, file)) <= 0:
                corrupted_files.append(file)
                continue
            try:
                data, _ = soundfile.read(join(root_dir, file))
            except:
                corrupted_files.append(file)
            if len(data) <= 0:
                corrupted_files.append(file)

    print()
    print("Done checking SWC Dataset")
    print("=====================")

    with open('swc_corrupted.txt', 'w') as f:
        for file in corrupted_files:
            f.write("%s\n" % file)





def gen_swc_csv(root_dir = dir):

    csv = []

    with open("transcriptions.txt", 'r') as f:
        lines = f.readlines()

    i=0
    for line in lines:
        i+=1
        file_name = line.split(" ", 1)[0]
        file_text = line.split(" ", 1)[1]

        if len(file_text == 1):
            continue

        trans = clean_sentence(file_text)
        file_path = os.path.join(root_dir, file_name + ".wav")
        csv.append( (file_path, trans) )
        print("File " +  str(i) + " / " +str(len(lines)), end='\r')

    print()
    print("Writing CSV File:")
    df = pandas.DataFrame(data=csv)
    output_file = "/speech/swc_all.csv"
    df.to_csv(output_file, header=False, index=False, sep=",")

    #csv_test = csv_output[0:5000]
    #csv_train = csv_output[5901:]        
    
    #df = pandas.DataFrame(data=csv_train)
    #output_file = "/data/home/GPUAdmin1/asr/train_csvs/swc_train.csv"
    #df.to_csv(output_file, index=False, sep=",")
    
    #df = pandas.DataFrame(data=csv_test)
    #output_file = "/data/home/GPUAdmin1/asr/test_csvs/swc_test.csv"
    #df.to_csv(output_file, index=False, sep=",")





def main():
    #convert_to_wav()
    #segment_wav()
    gen_swc_csv()
    #gen_corrupted_list_swc()

if __name__ == "__main__":
    main()
