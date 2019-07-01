#!/bin/bash

python -m multiproc train.py \
--train-manifest "/home/GPUAdmin1/asr/train.csv" \
--val-manifest "/home/GPUAdmin1/asr/dev.csv" \
--epochs 40 \
--checkpoint \
--checkpoint-per-batch 200 \
--save-folder "/speech/ds_pytorch_chkpts_600/" \
--hidden-layers 3 \
--hidden-size 700 \
--cuda \
--model-path "/speech/ds_pytorch_models_600/deepspeech_final.pth"


Training Summary Epoch: [1]     Time taken (s): 24165   Average Loss 43.878
100%|█████████████████████████████████████████████████████████████| 269/269 [05:47<00:00,  1.66it/s]
Validation Summary Epoch: [1]   Average WER 67.733      Average CER 19.650
Learning rate annealed to: 0.000273

Training Summary Epoch: [1]     Time taken (s): 7283    Average Loss 35.449
100%|█████████████████████████████████████████████████████████████| 269/269 [08:49<00:00,  1.08it/s]
Validation Summary Epoch: [1]   Average WER 76.938      Average CER 27.503