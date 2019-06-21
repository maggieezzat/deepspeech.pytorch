

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = "~/asr/"

#os.chdir(os.path.expanduser("~/asr/"))
#print(os.getcwd())
#os.chdir("/home/GPUAdmin1/asr/")
#print(os.getcwd())
#Where to store the wav files created to be changed on the VM
SWC_path = "~/asr/SWCData/"
with open("wav.txt") as f:
    lines = f.readlines()
lines = [l.strip() for l in lines]
for line in lines:
    #print(line[16:-3]+SWC_path+line[0:15]+".wav")
    os.system(line[16:-3]+SWC_path + line[0:15] + ".wav")
    #exit(0)
    #os.system("rm -r " + dir_path + "/".join(line[20:].split("/")[0:5]))

