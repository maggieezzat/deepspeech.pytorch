#!/bin/bash
wavfolder=/home/hamahmi/wav/
for foldername in /home/hamahmi/Korpus/*/; do
    fn=$(basename -- "$foldername")
    mkdir -p $wavfolder$fn
    python3 movie_csv.py --dirmovie $foldername --dircsv "/home/hamahmi/output.csv" --dirseg $wavfolder$fn
done
