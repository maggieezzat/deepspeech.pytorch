#!/bin/bash
wavfolder=/speech/movieswavs/
for foldername in /speech/Movies/*/; do
    fn=$(basename -- "$foldername")
    mkdir -p $wavfolder$fn
    python3 /data/home/GPUAdmin1/asr/deepspeech.pytorch/data/movies/movie_csv.py --dirmovie $foldername --dircsv "/speech/movieswavs/movies.csv" --dirseg $wavfolder$fn
done
