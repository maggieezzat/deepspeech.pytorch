import os
import re
import csv
import pandas

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from clean_text import clean_sentence

#dir = "/speech/common_voice_de/"
dir = "C:/Users/MaggieEzzat/Desktop/sv-SE/"

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
    #output_file = "/data/home/GPUAdmin1/asr/train_csvs/common_voice_train.csv"
    output_file = os.path.join(root_dir, "common_voice_train.csv")
    df.to_csv(output_file, header=False, index=False, sep=",")
     
    df = pandas.DataFrame(data=test_data)
    #output_file = "/data/home/GPUAdmin1/asr/dev_csvs/common_voice_test.csv"
    output_file = os.path.join(root_dir, "common_voice_test.csv")
    df.to_csv(output_file, header=False, index=False, sep=",")
    
    df = pandas.DataFrame(data=dev_data)
    #output_file = "/data/home/GPUAdmin1/asr/test_csvs/common_voice_dev.csv"
    output_file = os.path.join(root_dir, "common_voice_dev.csv")
    df.to_csv(output_file, header=False, index=False, sep=",")





def main():
    gen_common_voice_csv()

if __name__ == "__main__":
    main()