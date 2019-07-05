import csv
from clean_text import clean_sentence

rootdir = "/data/home/GPUAdmin1/asr/"
files = [rootdir+"train_csvs/M-AILABS_train.csv",rootdir+"train_csvs/cv_train.csv","/speech/german-speechdata-package-v2/SentencesAndIDs.cleaned.txt",
rootdir+"test_csvs/cv_test.csv",rootdir+"dev_csvs/cv_dev.csv"]

sentences = []
for file_dir in files:
    if(".csv" in file_dir):
        with open(file_dir) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                sentences.append(row[1] +"\n")
    else:
        with open(file_dir, "r") as text:
            for line in ins:
                sent = clean_sentence(line.split(" ",1)[1])
                sentences.append(sent+"\n")



sent_set = set(sentences)
corpus = open("corpus.txt","w")
corpus.writelines()

