from pydub import AudioSegment


with open("segments", 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

#for line in lines:


t_line = lines[0]
t_line = t_line.split(' ')
old_file = t_line[1]
new_file = t_line[0]
t1 = float(t_line[2])
t2 = float(t_line[3])
#t1 = 1038
#t2 = 1042


newAudio = AudioSegment.from_wav( old_file +".wav")
newAudio = newAudio[t1:t2]
newAudio.export(new_file + '.wav', format="wav")