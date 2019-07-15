import os
from clean_text import clean_sentence

rootdir = "/lm_corpus/web_sent_5M/"
sentences =[]
i=1
for file_name in os.listdir(rootdir):
    if(file_name.endswith("deu-at_web_2014_1M-sentences.txt")):
        with open(rootdir+file_name, "r") as text:
            c = 0
            for line in text:
                c+=1
                print(str(c) + " / 1000000" , end = '\r')
                if len(line.split(" ",1)) <= 1:
                        continue
                sent = clean_sentence(line.split(" ",1)[1])
                sentences.append(sent+"\n")
        print()
        print("File "+ str(i) +" done")
        i+=1
        print(file_name + "\n")



sent_set = set(sentences)
print(len(sent_set))
corpus = open("/lm_corpus/web_sent_5M.txt","w")
corpus.writelines(sent_set)