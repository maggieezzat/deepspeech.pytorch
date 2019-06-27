#!/bin/bash
foldername="/speech/common_voice_de/clips/"
outputfolder="/speech/common_voice_de/wav_files/"
FILECOUNT=$(find $foldername -type f | wc -l)
count=1
for filename in "/speech/common_voice_de/clips/"*; do
    fn=$(basename -- "$filename")
    echo -ne $count / $FILECOUNT '\r'
    ((count++))
    sox $foldername$fn -r 16000 -c 1 -b 16 "$outputfolder${fn%???}wav"	
done
echo "=-=-=-=-=-=Done=-=-=-=-=-="