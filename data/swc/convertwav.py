import os

dir_path = os.path.dirname(os.path.realpath(__file__))
#Where to store the wav files created to be changed on the VM
SWC_path = "~/asr/data"
with open(dir_path + "/wav.txt") as f:
    lines = f.readlines()
lines = [l.strip() for l in lines]
for line in lines:
    os.system(line[16:-3]+"~/Desktop/swc/" + line[0:15] + ".wav")
    os.system("rm -r " + dir_path + "/" + "/".join(line[20:].split("/")[0:5]))
