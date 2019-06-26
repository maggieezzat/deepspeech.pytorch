# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from os import listdir, remove
from os.path import isfile, join
import soundfile

import codecs
import fnmatch
import os
import sys
import tarfile
import tempfile
import unicodedata

from xml.etree import cElementTree as ET
from xml.dom import minidom
import re
import string
import pandas
from six.moves import urllib
import wget

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from clean_text import clean_sentence


download_dir = "/speech/"
#download_dir = "C:/Users/MaggieEzzat/Desktop/"
directory = "/speech/german-speechdata-package-v2/"
tuda_url = "http://speech.tools/kaldi_tuda_de/german-speechdata-package-v2.tar.gz"



def download_and_extract(down_dir=download_dir, url=tuda_url):
    """Download and extract tuda-de dataset.

  Args:
    directory: the directory where to extract the downloaded folder.
    url: the url to download the data file.
  """

    wget.download(url, down_dir)  
    tar_filepath = os.path.join(down_dir, "german-speechdata-package-v2.tar.gz")
    #with tarfile.open(tar_filepath, "r") as tar:
    #    tar.extractall(down_dir)

def generate_second_list_corrupted_files(directory):
    """Generate corrupted2.txt from Tuda Data
        corrupted.txt i.e. first corrupted list was taken from here: 
        https://github.com/uhh-lt/kaldi-tuda-de/blob/master/s5_r2/local/cleanup/problematic_wavs.txt 
    """
    
    paths = ["test", "dev", "train"]
    corrupted_files = []

    for path in paths:
        files = [
            f
            for f in listdir(join(directory, path))
            if isfile(join(directory, path, f))
        ]

        total_files=len(files)
        processed_files = 0
        
        for file in files:
            processed_files+=1
            if ".wav" in file: 
                print("Checking files from " + path + " set " + str(processed_files) + "/" + str(total_files), end="\r")
                if os.path.getsize(join(directory, path, file)) <= 0:
                    corrupted_files.append(file)
                    continue
                data, _ = soundfile.read(join(directory, path, file))
                if len(data) <= 0:
                    corrupted_files.append(file)

        print()
        print("Done checking " + path + " set")
        print("=====================")

    with open('corrupted2.txt', 'w') as f:
        for file in corrupted_files:
            f.write("%s\n" % file)
    
    print("Done writing corrupted2.txt" +
    "Together with corrupted.txt they contain all corrupted files in Tuda-De")
    print("=====================")


def delete():

    cor = []
    corrupted_lists = ["corrupted.txt", "corrupted2.txt"]
    for corrupted_list in corrupted_lists:
        txtCor = os.path.join(os.path.dirname(__file__), corrupted_list)
        with open(txtCor) as corfile:
            content = corfile.readlines()
        content = [x.strip() for x in content]
        for jk in range(len(content)):
            if corrupted_list == "corrupted.txt":
                cor.append(content[jk][37:57])
            else:
                cor.append(content[jk])


    paths = ["test", "dev", "train"]
    for path in paths:
        files = [
            f
            for f in listdir(join(directory, path))
            if isfile(join(directory, path, f))
        ]
        total_files = len(files)
        processed_files = 0
    
        for file in files:
            processed_files+=1
            print("Deleting from " + path + " " + str(processed_files) + "/" + str(total_files), end="\r")
            if ".wav" in file:
                #remove 3 microphones out of 5 
                #remove the mic condition if you want to keep all mics
                #use all mics
                #if (("Kinect-Beam" in file) or ("Yamaha" in file) or ("Samson" in file)):
                #    remove(join(directory, path, file))
                #else:
                for crptd in cor:
                    if (crptd in file):
                        remove(join(directory, path, file))
                        break

            #fix a corrupted xml file in dev set =)
            if path == "dev" and ".xml" in file:
                fix_xml = False
                xml_name = ""
                newContent = ""
                with open(join(directory, path, file), 'r+', encoding="utf8") as f:
                    content = f.readlines()
                    content = [x.strip() for x in content]
                    for con in content:
                        if con.find("<html><body>") != -1:
                            newContent = con[12:]
                            newContent = newContent[:-14]
                            fix_xml = True
                            xml_name = file
                if fix_xml:
                    os.remove(join(directory, path, xml_name))
                    with open(join(directory, path, xml_name), 'w', encoding="utf8") as f:
                        f.write("%s" % newContent)
                    fix_xml = False
                    xml_name = ""
                    newContent = ""


        print()
        print("Done deleting from " + path + " " + str(processed_files) + "/" + str(total_files))
        print("=====================")


def generate_csv():
 
    paths = ["test", "dev", "train"]
    
    for path in paths:
        
        csv = []
        files = [
            f
            for f in listdir(join(directory, path))
            if isfile(join(directory, path, f))
        ]
        dir_path = os.path.join(directory, path)
        processed_files = 0
        total_files = len(files)

        for file in files:

            file_path = os.path.join(dir_path, file)
            processed_files+=1
            print("Processing " + path + " " + str(processed_files) + "/" + str(total_files), end="\r")
            if file.endswith(".xml"):
                tree = ET.parse(file_path)
                recording = tree.getroot()
                sent = recording.find("cleaned_sentence")
                sent = sent.text.lower()
                transcript = clean_sentence(sent)


                file_xml, _ = file.split(".", 1)
                found = 0
                for wav_file in files:
                    if wav_file.startswith(file_xml) and wav_file.endswith(".wav"):

                        wav_file_dir = os.path.join(dir_path, wav_file)
                        csv.append((wav_file_dir, transcript))
                        found += 1
                    #remove that check if you keep more than 2 microphones    
                    #if found >= 2:
                    if found >= 5:
                        break

        print()
        output_file = os.path.join(directory, path + ".csv")

        with open(output_file, 'w') as f:
            for line in csv:
                f.write(line[0]+","+line[1] + "\n")

        
        print("Successfully generated csv file {}.csv".format(path))
        print("=====================")


def main():

    download_and_extract(download_dir,tuda_url)

    #cor2 = os.path.join(os.path.dirname(__file__), "corrupted2.txt")
    #exists = os.path.isfile(cor2)
    #if exists:
    #    print("corrupted list 2 already found")
    #else:
    #    generate_second_list_corrupted_files(directory)
    
    #delete()
    #generate_csv()
   


if __name__ == "__main__":
    main()
