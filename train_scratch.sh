#!/bin/bash

python -m multiproc train.py \
--train-manifest "/home/GPUAdmin1/asr/train.csv" \
--val-manifest "/home/GPUAdmin1/asr/test.csv" \
--epochs 40 \
--checkpoint \
--checkpoint-per-batch 50 \
--save-folder "/speech/ds_pytorch_chkpts_600/" \
--hidden-layers 3 \
--hidden-size 700 \
--cuda \
--model-path "/speech/ds_pytorch_models_600/deepspeech_final.pth"
