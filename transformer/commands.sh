USR_DIR=/data/home/GPUAdmin1/asr/deepspeech.pytorch/transformer/
PROBLEM=asr_correction
MODEL=transformer
HPARAMS=transformer_big
DATA_DIR=$HOME/t2t_data

TMP_DIR=/tmp/t2t_datagen
mkdir -p $DATA_DIR $TMP_DIR

HPARAMS=transformer_base_single_gpu

t2t-datagen \
  --t2t_usr_dir=$USR_DIR \
  --data_dir=$DATA_DIR \
  --tmp_dir=$TMP_DIR \
  --problem=$PROBLEM


t2t-trainer \
  --generate_data \
  --data_dir=~/t2t_data \
  --output_dir=~/t2t_train/asr_correction \
  --problem=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --train_steps=100000 \
  --eval_steps=100 \
  --t2t_usr_dir=$USR_DIR \
  --export_saved_model=True



 CUDA_VISIBLE_DEVICES=0 t2t-trainer \
  --data_dir=~/t2t_data \
  --output_dir=~/t2t_train/asr_correction \
  --problem=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --train_steps=100000 \
  --t2t_usr_dir=$USR_DIR


BEAM_SIZE=4
ALPHA=0.6
DECODE_FILE=/data/home/GPUAdmin1/asr_correction_data_to_decode.txt

$DATA_DIR/asr_correction_data_to_decode.txt


  t2t-decoder \
    --data_dir=$DATA_DIR \
    --problem=$PROBLEM \
    --model=$MODEL \
    --hparams_set=$HPARAMS \
    --output_dir=~/t2t_train/asr_correction \
    --decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA" \
    --decode_from_file=$DECODE_FILE \
    --decode_to_file=/data/home/GPUAdmin1/asr/asr_correction_decoder.txt \
    --t2t_usr_dir=$USR_DIR