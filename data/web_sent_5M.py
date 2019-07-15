import os
from clean_text import clean_sentence

rootdir = "/lm_corpus/web_sent_5M/"
sentences =[]
i=1
for file in os.listdir(rootdir):
    if(".txt" in file):
         with open(rootdir+file, "r") as text:
            for line in text:
                sent = clean_sentence(line.split(" ",1)[1])
                sentences.append(sent+"\n")
         print("File "+ str(i) +" done",end = "\r")
         i+=1



sent_set = set(sentences)
print(len(sent_set))
corpus = open("/lm_corpus/web_sent_5M.txt","w")
corpus.writelines(corpus)