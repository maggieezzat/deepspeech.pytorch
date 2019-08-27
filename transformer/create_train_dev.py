import csv
import pandas

file_paths = ["/speech/epoch13_5gram_transcriptions/ep13_5gm_dev_transcriptions.csv",
"/speech/epoch13_5gram_transcriptions/ep13_5gm_single_speaker_transcriptions.csv"]


all_data = []
for file_dir in file_paths:
    with open(file_dir) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        filename = row[0]
                        transcript = row[1]
                        all_data.append((filename,transcript))

count =1
old_file = all_data[0][0]
dev = []
train = []
for i in range(len(all_data)):
    if(old_file ==all_data[i][0]):
        if(count != 10):
            train.append((all_data[i]))
        else:
            dev.append(all_data[i])
    else:
        old_file = all_data[i][0]
        if(count == 10):
            count =0
        count+=1
        if(count == 10):
             dev.append((all_data[i]))
        else:
             train.append((all_data[i]))
    print(str(i) +" / "+str(len(all_data)),end = "\r")


df = pandas.DataFrame(data=train)
    output_file = "/speech/epoch13_5gram_transcriptions/train/dev_single_speaker_train.csv"
    df.to_csv(output_file, header=False, index=False, sep=",")

df = pandas.DataFrame(data=dev)
    output_file = "/speech/epoch13_5gram_transcriptions/dev/dev_single_speaker_dev.csv"
    df.to_csv(output_file, header=False, index=False, sep=",")