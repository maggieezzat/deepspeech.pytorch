#!/bin/bash

python -m multiproc train.py \
--train-manifest "/home/GPUAdmin1/asr/german-speechdata-package-v2/train/train.csv" \
--val-manifest "/home/GPUAdmin1/asr/german-speechdata-package-v2/train/test.csv" \
--epochs 40 \
--checkpoint \
--checkpoint-per-batch 50 \
--save-folder "/home/GPUAdmin1/asr/ds_pytorch_chkpts" \
--continue-from "/home/GPUAdmin1/asr/ds_pytorch_chkpts/deepspeech_checkpoint_epoch_1_iter_110.pth" \
--hidden-layers 3 \
--hidden-size 700 \
--cuda
