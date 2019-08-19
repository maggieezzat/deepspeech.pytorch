USR_DIR=/data/home/GPUAdmin1/asr/deepspeech.pytorch/transformer/
PROBLEM=asr_correction
MODEL=transformer
HPARAMS=transformer_big
DATA_DIR=$HOME/t2t_data
OUT_DIR=/t2t_train/asr_correction
 
CUDA_VISIBLE_DEVICES=0 t2t-trainer \
--data_dir=$DATA_DIR \
--output_dir=$OUT_DIR \
--problem=$PROBLEM \
--model=$MODEL \
--hparams_set=$HPARAMS \
--train_steps=100000 \
--t2t_usr_dir=$USR_DIR