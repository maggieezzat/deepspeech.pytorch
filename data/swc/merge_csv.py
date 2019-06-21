import os
import pandas as pd
rootdir = "C:/Users/MariamDesouky/Desktop/train_csvs"

for file in os.listdir(rootdir):
    data = pd.concat([pd.read_csv(rootdir+ "/" + file)])


data.to_csv("C:/Desktop/train.csv", index=False, sep=",")

"""
rootdir = "~/asr/test_csvs"  

for file in os.listdir(rootdir):
    data = pd.concat([pd.read_csv(rootdir+ "/" + file)])
"""