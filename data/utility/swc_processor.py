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
    
    with open("/speech/SWC_German/segments.txt", 'r') as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]

    #for line in lines:
    t_line = lines[0]
    t_line = t_line.split(' ')
    old_file = t_line[1]
    new_file = t_line[0]
    t1 = float(t_line[2])
    t2 = float(t_line[3])


    newAudio = AudioSegment.from_wav( old_file +".wav")
    newAudio = newAudio[t1:t2]
    newAudio.export(new_file + '.wav', format="wav")


def main():
    convert_to_wav()
    #segment_wav()

if __name__ == "__main__":
    main()