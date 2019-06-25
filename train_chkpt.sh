#!/bin/bash

python -m multiproc train.py \
--visdom \
--train-manifest "/home/GPUAdmin1/asr/train.csv" \
--val-manifest "/home/GPUAdmin1/asr/test.csv" \
--epochs 40 \
--learning-anneal 10 \
--checkpoint \
--checkpoint-per-batch 50 \
--save-folder "/speech/test/" \
--continue-from "/speech/ds_pytorch_chkpts/$1" \
--hidden-layers 3 \
--hidden-size 700 \
--cuda \
--model-path "/speech/test/deepspeech_final.pth"
