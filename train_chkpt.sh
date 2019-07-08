#!/bin/bash

python -m multiproc train.py \
--train-manifest "/home/GPUAdmin1/asr/train.csv" \
--val-manifest "/home/GPUAdmin1/asr/dev.csv" \
--batch-size 14 \
--epochs 40 \
--checkpoint \
--checkpoint-per-batch 150 \
--save-folder "/speech/ds_pytorch_chkpts_lstm_5/" \
--continue-from "/speech/ds_pytorch_chkpts_lstm_5/$1" \
--hidden-layers 5 \
--hidden-size 800 \
--cuda \
--model-path "/speech/ds_pytorch_models_lstm_5/deepspeech_final.pth" \
--rnn-type "lstm"
