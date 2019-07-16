#!/bin/bash

root_dir=/lm_corpus/dewiki_nltk_segmented/
wiki=/lm_corpus/dewiki.txt

for dir in $root_dir; do
    for file in $(find $root_dir/$dir -maxdepth 1 -type f); do
        cat $file >> $wiki
    done
done
