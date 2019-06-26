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
rootdir = "E:/csv/"
data = pd.concat(
    [pd.read_csv(rootdir + "/" + file) for file in os.listdir(rootdir)],
    axis=0,
    sort=False,
)
data.to_csv("E:/csv/o.csv", index=False, encoding="utf-8-sig")

