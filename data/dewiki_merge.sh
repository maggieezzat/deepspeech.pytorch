#!/bin/bash

root_dir=/lm_corpus/dewiki_nltk_segmented/
wiki=/lm_corpus/dewiki.txt

for dir in $root_dir; do
    echo $dir
    for file in $(find $dir -maxdepth 1 -type f); do
        echo $file
        cat $file >> $wiki
    done
done
