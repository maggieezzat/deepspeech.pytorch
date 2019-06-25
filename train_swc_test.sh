#!/bin/bash

python -m multiproc train.py \
--train-manifest "/home/GPUAdmin1/asr/swc.csv" \
--val-manifest "/home/GPUAdmin1/asr/test.csv" \
--epochs 40 \
--checkpoint \
--checkpoint-per-batch 50 \
--save-folder "/speech/swc_test_chkpts/" \
--continue-from "/speech/ds_pytorch_chkpts/$1" \
--hidden-layers 3 \
--hidden-size 700 \
--cuda \
--model-path "/speech/swc_test_chkpts/deepspeech_final.pth"