#!/bin/bash

root_dir=/lm_corpus/dewiki_nltk_segmented/
wiki=/lm_corpus/dewiki.txt

for dir in $(find $root_dir -maxdepth 1 -type d); do
    for file in $(find $dir -maxdepth 1 -type f); do
        cat $file >> $wiki
    done
done
