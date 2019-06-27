from __future__ import print_function
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

    if not os.path.exists(valid_wav):
        os.makedirs(valid_wav)

    validated_tsv = os.path.join(root_dir, "validated.tsv")
    valid_data = []

    with open(validated_tsv) as f:
        lines = csv.reader(f, delimiter='\t')
        next(lines, None)
        total = len(list(lines))
        i=0
        for line in lines:
            i+=1
            src = os.path.join(root_dir, "clips", line[1]+".mp3")
            dst = os.path.join(valid_wav, line[1]+".wav")
            trans = clean_sentence(line[2])
            valid_data.append((dst, trans))
            # convert wav to mp3                                                            
            sound = AudioSegment.from_mp3(src)
            sound = sound.set_frame_rate(16000)
            sound.export(dst, format="wav")
            print(str(i), end='\r')
            print("Converting files: " + str(i) + " / " + str(total), end="\r")



    df = pandas.DataFrame(data=valid_data)
    output_file = "/data/home/GPUAdmin1/speech/common_voice_de/common_voice_valid_wav.csv"
    df.to_csv(output_file, header=False, index=False, sep=",")




def get_dict_speakers(root_dir = dir):

    validated_tsv = os.path.join(root_dir, "validated.tsv")
    speakers = set()

    with open(validated_tsv) as f:
        lines = csv.reader(f, delimiter='\t')
        next(lines, None)
        for line in lines:
            speakers.add(line[0])

    speakers_list = list(speakers)
    speakers_dict = dict(enumerate(speakers_list, start=0))
    return speakers_dict



def rename_utterances(root_dir = dir):

    valid_wav = os.path.join(root_dir, "valid_wav")

    validated_tsv = os.path.join(root_dir, "validated.tsv")
    valid_data = []

    speakers_dict = get_dict_speakers()
    #print(speakers_dict)
    #print(len(speakers_dict))
    #exit(0)

    with open(validated_tsv) as f:
        lines = csv.reader(f, delimiter='\t')
        next(lines, None)
        i=0
        for line in lines: 
            src = os.path.join(valid_wav, line[1]+".wav")
            client_id = line[0]
            speaker = speakers_dict[100]
            print(speaker)
            print(client_id)
            exit(0)
            dst = os.path.join(valid_wav, "utt_{0:0=6d}_spk{0:0=4d}.wav".format(i, speaker))
            os.rename(src, dst)
            i+=1
            




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
    #convert_to_wav()
    #get_num_of_speakers()
    rename_utterances()

if __name__ == "__main__":
    main()