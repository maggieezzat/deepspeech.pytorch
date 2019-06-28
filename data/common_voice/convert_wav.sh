#!/bin/bash



for filename in "/speech/common_voice_de/clips/"*; do
    fn=$(basename -- "$filename")	
    echo $fn
    #sox $foldername$fn -r 16000 -c 1 -b 16 "$foldername-new$fn"	
done

