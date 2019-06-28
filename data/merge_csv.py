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
for rootdir in dirs:
    data = pd.concat(
        [pd.read_csv("/data/home/GPUAdmin1/asr/"+rootdir + "/" + file) for file in os.listdir("/data/home/GPUAdmin1/asr/"+rootdir)],
        axis=0,
        sort=False,
    )
    directory = rootdir.split("_")
    data.to_csv("/data/home/GPUAdmin1/asr/"+directory[0]+".csv", index=False, encoding="utf-8-sig")

