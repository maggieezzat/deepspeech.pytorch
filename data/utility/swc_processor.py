import os
from pydub import AudioSegment




def convert_to_wav():
    
    SWC_path = "/speech/SWC_wav/"

    if not os.path.exists(SWC_path):
        os.makedirs(SWC_path)
    
    with open("/speech/SWC_German/wav.txt") as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]
    for line in lines:
        os.system(line[16:-3] + SWC_path + line[0:15] + ".wav")





def segment_wav():

    data_dir = "/speech/SWC_wav/"

    segmented_files_dir = "/speech/spoken_wikipedia_german/"
    if not os.path.exists(segmented_files_dir):
        os.makedirs(segmented_files_dir)
    
    with open("/speech/SWC_German/segments.txt", 'r') as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]

    i=0
    for line in lines:
        i+=1
        if i < 35000:
            print("Skipping " + str(i), end='\r')
            continue
        line = line.split(' ')
        old_file = os.path.join(data_dir, line[1])
        new_file = os.path.join(segmented_files_dir, line[0])
        t1 = float(line[2]) * 1000
        t2 = float(line[3]) * 1000

        newAudio = AudioSegment.from_wav( old_file +".wav")
        newAudio = newAudio[t1:t2]
        newAudio.export(new_file + '.wav', format="wav")
        
        print(str(i) + "/ 35000", end='\r')


def main():
    #convert_to_wav()
    segment_wav()

if __name__ == "__main__":
    main()
