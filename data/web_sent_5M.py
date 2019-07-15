import os
from clean_text import clean_sentence

rootdir = "/lm_corpus/web_sent_5M/"
sentences =[]
i=1
for file_name in os.listdir(rootdir):
    if(file_name.endswith(".txt")):
         with open(rootdir+file_name, "r") as text:
            for line in text:
                print(".")
                sent = clean_sentence(line.split(" ",1)[1])
                sentences.append(sent+"\n")
         print("File "+ str(i) +" done")
         i+=1



sent_set = set(sentences)
print(len(sent_set))
corpus = open("/lm_corpus/web_sent_5M.txt","w")
corpus.writelines(corpus)