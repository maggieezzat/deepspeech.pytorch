import os

file_dir ="/data/home/GPUAdmin1/asr/train.csv"
with open(file_dir) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
         path = row[0]
         if(os.path.exists(path)):
             continue
         else:
             print(path)

