# coding=utf-8

from pydub import AudioSegment
from argparse import ArgumentParser
import os
import re
import string

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from clean_text import clean_sentence

# ====== Flags ======
parser = ArgumentParser()

parser.add_argument("--dirmovie", metavar="DIR", default="/home/hamahmi/dark/Dark")
parser.add_argument(
    "--dircsv", metavar="DIR", default="/home/hamahmi/dark/Dark/output.csv"
)
parser.add_argument("--dirseg", metavar="DIR", default="/home/hamahmi/dark/wavs/")

args = parser.parse_args()

# =================== functions ===================


def getms(time):
    time = time.split(":")
    ms = int(time[0]) * 3600000
    ms += int(time[1]) * 60000
    seconds = time[2].split(",")
    ms += int(seconds[0]) * 1000
    ms += int(seconds[1])
    return ms


def clean(string, start, end=None):
    # future work : take a list of start and end to call just once
    # the start and the end char are the same z.B : '♪'
    if end == None:
        end = start
    tmp = string.split(start, 1)
    out = tmp[0]
    tmp = tmp[1].split(end, 1)
    # if there is more than one occurance
    if start in tmp[1] and end in tmp[1]:
        out += clean(tmp[1], start, end)
    else:
        out += tmp[1]
    return out
    # --future work : take a list of start and end to call just once
    tmp = string.split(start, 1)
    out = tmp[0]
    tmp = tmp[1].split(end, 1)
    # if there is more than one occurance
    if start in tmp[1] and end in tmp[1]:
        out += cleanh(tmp[1], start, end)
    else:
        out += tmp[1]
    return out




# =================== Main ===================
"""
for this code to run correctly the data should be as follow:
directory_
          |--Transcript_    (i.e full path = transcript_dir)
          |             |--abcd1.srt (or .txt)
          |             |--abcd2.srt ...
          |             | ...
          |--Audio_         (i.e full path = audio_dir)
          |        |--abcd1.wav
          |        |--abcd2.wav ...
          |        |--...
          (note that wav file must have the same name of its corresponding transcription file)
          
"""
directory = args.dirmovie
transcript_dir = os.path.join(directory, "Transcript/")
audio_dir = os.path.join(directory, "Audio/")
# put where you want the csv file
output_csv = args.dircsv
# put where you want the wavs to be saved (folder)
output_segments = args.dirseg
csv = []
# loop over all transcription files and create csv
for file in os.listdir(transcript_dir):
    big_wav_dir = os.path.join(audio_dir, (file[:-3] + "wav"))
    big_wav = AudioSegment.from_wav(big_wav_dir)
    with open(os.path.join(transcript_dir, file), "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]
    sequences = []
    tmp = []
    # sequences is list of each transcript for a wav segment
    for line in lines:
        if line == "":
            sequences.append(tmp)
            tmp = []
        else:
            tmp.append(line)
    # process the transcription
    for s in sequences:
        number = int(s[0].strip())
        print(
            "Processing file "
            + file[:-4]
            + " : "
            + str(int((number / len(sequences)) * 100))
            + "%",
            end="\r",
        )
        filename = file[:-4] + "_" + str(number) + ".wav"
        time = s[1]
        time = time.split(" ")
        timefrom = getms(time[0])
        timeto = getms(time[-1])
        transcriptl = s[2:]
        transcript = ""
        for t in transcriptl:
            transcript += t + " "
        # --TODO remove things between [] and ♪
        if "[" in transcript and "]" in transcript:
            transcript = clean(transcript, "[", "]")
        if "(" in transcript and ")" in transcript:
            transcript = clean(transcript, "(", ")")
        if "<" in transcript and ">" in transcript:
            transcript = clean(transcript, "<", ">")
        if "♪" in transcript:
            transcript = clean(transcript, "♪")

        transcriptclean = clean_sentence(transcript)
        # --TODO if the whole wav is non talk igneore it i.e continue
        if (
            transcriptclean.strip() == ""
            or transcriptclean.strip() == "netflix präsentiert"
            or transcriptclean.strip() == "eine netflix original serie"
        ):
            # non talk sounds, ignore them.
            continue
        # --TODO segment the wav file and put it in the csv
        segment_wav = big_wav[timefrom : timeto + 1]
        segment_wav_dir = os.path.join(output_segments, filename)
        segment_wav.export(segment_wav_dir, format="wav")
        csv.append((segment_wav_dir, transcriptclean))
    print()

with open(output_csv, "w") as f:
    for line in csv:
        print(
            "Saving into CSV file : "
            + str(int(((csv.index(line) + 1) / len(csv)) * 100))
            + "%",
            end="\r",
        )
        f.write(line[0] + "," + line[1] + "\n")
