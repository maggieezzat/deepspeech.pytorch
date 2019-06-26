import os
import wave
import datetime
from pydub import AudioSegment

#"spoken_wikipedia_german","M-AILABS",
datafolders = ["spoken_wikipedia_german","M-AILABS","german-speechdata-package-v2"]
time = datetime.timedelta(milliseconds = 0)
for dir in datafolders:
     for subdir, dirs, files in os.walk("/speech/"+dir):
         for file in files:
             if(file.endswith(".wav")):
                    file_dir = os.path.join(subdir, file)
                    millis = len(AudioSegment.from_wav(file_dir))
                    time += datetime.timedelta(milliseconds= millis)
                    print(file,end='\r')
         print("ended "+ subdir)

print()
print(time.seconds/3600 + time.days*24)


  
