import os
import re
import csv
import pandas
from pydub import AudioSegment

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from clean_text import clean_sentence

dir = "/speech/common_voice_de/"


def convert_to_wav(root_dir = dir):

    valid_wav = os.path.join(root_dir, "valid_wav")

    #if not os.path.exists(valid_wav):
    #    os.makedirs(valid_wav)

    validated_tsv = os.path.join(root_dir, "validated.tsv")
    valid_data = []

    #print(validated_tsv)

    with open(validated_tsv) as f:
        lines = csv.reader(f, delimiter='\t')
        next(lines, None)
        i=0
        for line in lines:
            i+=1
            if i == 1:
                continue
            #print("hi")
            src = os.path.join(root_dir, "clips", line[1]+".mp3")
            dst = os.path.join(valid_wav, line[1][1:7]+".wav")
            print(src)
            print(dst)
            trans = clean_sentence(line[2])
            valid_data.append((dst, trans))
            # convert wav to mp3                                                            
            sound = AudioSegment.from_mp3(src)
            sound.export(dst, format="wav")
            
            print("Converting files: " + str(i) + " / 277603", end="\r")



    df = pandas.DataFrame(data=valid_data)
    output_file = "/data/home/GPUAdmin1/asr/common_voice_all.csv"
    df.to_csv(output_file, header=False, index=False, sep=",")







def gen_common_voice_csv(root_dir = dir):


    train_tsv = os.path.join(root_dir, "train.tsv")
    test_tsv =  os.path.join(root_dir, "test.tsv")
    dev_tsv =  os.path.join(root_dir, "dev.tsv")
    validated_tsv = os.path.join(root_dir, "validated.tsv")

    valid_data = []
    train_data = []
    dev_data = []
    test_data = []

    with open(validated_tsv) as f:
        lines = csv.reader(f, delimiter='\t')
        next(lines, None)
        for line in lines:
            print(line)
            path = os.path.join(root_dir, "clips", line[1])
            trans = clean_sentence(line[2])
            valid_data.append((path, trans))


    with open(train_tsv) as f:
        lines = csv.reader(f, delimiter='\t')
        next(lines, None)
        for line in lines:
            path = os.path.join(root_dir, "clips", line[1])
            trans = clean_sentence(line[2])
            train_data.append((path, trans))
        for item in train_data:
            if item not in valid_data:
                train_data.remove(item)

    with open(test_tsv) as f:
        lines = csv.reader(f, delimiter='\t')
        next(lines, None)
        for line in lines:
            path = os.path.join(root_dir, "clips", line[1])
            trans = clean_sentence(line[2])
            test_data.append((path, trans))
        for item in test_data:
            if item not in valid_data:
                test_data.remove(item)

    with open(dev_tsv) as f:
        lines = csv.reader(f, delimiter='\t')
        next(lines, None)
        for line in lines:
            path = os.path.join(root_dir, "clips", line[1])
            trans = clean_sentence(line[2])
            dev_data.append((path, trans))
        for item in dev_data:
            if item not in valid_data:
                dev_data.remove(item)



    df = pandas.DataFrame(data=train_data)
    output_file = "/data/home/GPUAdmin1/asr/train_csvs/common_voice_train.csv"
    df.to_csv(output_file, header=False, index=False, sep=",")
     
    df = pandas.DataFrame(data=test_data)
    output_file = "/data/home/GPUAdmin1/asr/test_csvs/common_voice_test.csv"
    df.to_csv(output_file, header=False, index=False, sep=",")
    
    df = pandas.DataFrame(data=dev_data)
    output_file = "/data/home/GPUAdmin1/asr/dev_csvs/common_voice_dev.csv"
    df.to_csv(output_file, header=False, index=False, sep=",")


def gen_corrupted_list_cv(root_dir=dir):
    
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



def main():
    #gen_common_voice_csv()
    convert_to_wav()

if __name__ == "__main__":
    main()