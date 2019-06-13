#!/bin/bash

python -m multiproc train.py \
--train-manifest "/home/GPUAdmin1/asr/german-speechdata-package-v2/train.csv" \
--val-manifest "/home/GPUAdmin1/asr/german-speechdata-package-v2/test.csv" \
--epochs 40 \
--checkpoint \
--checkpoint-per-batch 100 \
--save-folder "/home/GPUAdmin1/asr/ds_pytorch_chkpts/" \
--hidden-layers 3 \
--hidden-size 700 \
--cuda \
--model-path "/home/GPUAdmin1/asr/ds_pytorch_models/"