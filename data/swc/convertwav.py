import os

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/wav.txt") as f:
    lines = f.readlines()
lines = [l.strip() for l in lines]
for line in lines:
    os.system(line[16:-3] + line[0:15] + ".wav")
    os.system("sudo rm -r " + dir_path + "/" + "/".join(line[20:].split("/")[0:5]))