import os
import pandas as pd


#NOTE: 2 ADDITIONAL COMMAS BETWEEN EACH UTTERANCE IS ADDED NO TIME TO DEBUG REMOVED MANUALLY
"""
#TRAIN
rootdir = "C:/Users/MariamDesouky/Desktop/train_csvs"
data = pd.concat([pd.read_csv(rootdir+ "/" + file) for file in os.listdir(rootdir) ],axis=0,sort=False)
data.to_csv("C:/Users/MariamDesouky/Desktop/train.csv", index=False, sep=",")
"""

#TEST
rootdir = "E:/csv/"  
data = pd.concat([pd.read_csv(rootdir+ "/" + file) for file in os.listdir(rootdir) ],axis=0,sort=False)
data.to_csv("E:/csv/o.csv", index=False, encoding='utf-8-sig')