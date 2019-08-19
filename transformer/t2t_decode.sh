  
USR_DIR=/data/home/GPUAdmin1/asr/deepspeech.pytorch/transformer/
PROBLEM=asr_correction
MODEL=transformer
HPARAMS=transformer_big
DATA_DIR=$HOME/t2t_data
OUT_DIR=/t2t_train/asr_correction
  
BEAM_SIZE=4
ALPHA=0.6
DECODE_FILE=$1
OUT_FILE=$2

CUDA_VISIBLE_DEVICES=1 t2t-decoder \
--data_dir=$DATA_DIR \
--problem=$PROBLEM \
--model=$MODEL \
--hparams_set=$HPARAMS \
--output_dir=$OUT_DIR \
--decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA" \
--decode_from_file=$DECODE_FILE \
--decode_to_file=$OUT_FILE \
--t2t_usr_dir=$USR_DIR