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


dir = "/speech/german-single-speaker-speech-dataset/"

def gen_csv(root_dir = dir):

    csv_list = []

    trans = root_dir + "transcript.txt"
    error = 0
    with open(trans, 'r') as f:
        lines = csv.reader(f, delimiter='|')

        i=0
        for line in lines:
            i+=1
            path = join(root_dir, line[0])
            text = line[2]

            clean_text = clean_sentence(text)
            csv_list.append( (path, clean_text) )
            print("File " +  str(i) + " / 7427", end='\r')

    print()
    print("Writing CSV File:")
    df = pandas.DataFrame(data=csv_list)
    output_file = "/home/GPUAdmin1/asr/train_csvs/single_speaker.csv"
    df.to_csv(output_file, header=False, index=False, sep=",")




def main():
    gen_csv()

if __name__ == "__main__":
    main()