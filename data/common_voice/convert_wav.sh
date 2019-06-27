#!/bin/bash

for i in /speech/common_voice_de/clips/*.mp3
do
    sox "$i" "/speech/common_voice_de/wav_files/$(basename -s .mp3 "$i").wav"
done