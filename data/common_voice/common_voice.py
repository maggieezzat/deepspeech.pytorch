from __future__ import print_function
import os
import re
import csv
import pandas
from pydub import AudioSegment
import shutil

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
    speakers_dict = {x:y for y,x in enumerate(speakers_list)}
    return speakers_dict



def rename_utterances_and_gen_csv(root_dir = dir):

    wav_files = os.path.join(root_dir, "wav_files")
    valid_wav = os.path.join(root_dir, "valid_wav")
    
    validated_tsv = os.path.join(root_dir, "validated.tsv")
    
    csv_data = []
    speakers_dict = get_dict_speakers()


    with open(validated_tsv) as f:
        lines = csv.reader(f, delimiter='\t')
        next(lines, None)
        c = 0
        i=0
        for line in lines:  
            c+=1
            if c == 795 or c == 796 or c == 794: 
                client_id = line[0]
                speaker = speakers_dict.get(client_id)
                print(str(speaker), client_id)
            
            
                src = os.path.join(wav_files, line[1]+".wav")
                
                dst = os.path.join(valid_wav, "utt_{0:0=6d}".format(i) + "_spk{0:0=4d}.wav".format(speaker))
                shutil.copy(src, dst)
                
                trans = clean_sentence(line[2])
                csv_data.append( (dst, trans) )
                i+=1
                print("Renaming: " + str(i) + " / 277603 ", end="\r")
            elif c > 796:
                exit(0)
            else:
                continue

    #df = pandas.DataFrame(data=csv_data)
    #output_file = "/data/home/GPUAdmin1/speech/common_voice_de/common_voice_valid_wav.csv"
    #df.to_csv(output_file, header=False, index=False, sep=",")
            




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
    #convert_to_wav()
    #get_num_of_speakers()
    rename_utterances_and_gen_csv()

if __name__ == "__main__":
    main()