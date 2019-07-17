import os
import pandas as pd


# NOTE: at the begining of the csv the columns MUST have the same name to be merged correctly (i.e. the first line of all csvs to be merged must be the same)
"""
#TRAIN
rootdir = "C:/Users/MariamDesouky/Desktop/train_csvs"
data = pd.concat([pd.read_csv(rootdir+ "/" + file) for file in os.listdir(rootdir) ],axis=0,sort=False)
data.to_csv("C:/Users/MariamDesouky/Desktop/train.csv", index=False,encoding='utf-8-sig')
"""

# TEST
dirs = ["train_csvs","dev_csvs","test_csvs"]
for dir in dirs:
    data = pd.concat(
        [pd.read_csv("/data/home/GPUAdmin1/asr/"+dir + "/" + file) for file in os.listdir("/data/home/GPUAdmin1/asr/"+dir)],
        axis=1,
        sort=False,
    )
    directory = dir.split("_")
    #data.to_csv("/data/home/GPUAdmin1/asr/"+directory[0]+".csv", index=False, header=False, encoding="utf-8-sig")
    data.to_csv("/speech/"+directory[0]+".csv", index=False, header=False, encoding="utf-8-sig")


