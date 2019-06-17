import os
with open("data/swc/wav.txt") as f:
    lines = f.readlines()
lines = [l.strip() for l in lines]
for line in lines:
    os.system(line[16:-3] + "data/swc/" + line[0:15] + ".wav")
