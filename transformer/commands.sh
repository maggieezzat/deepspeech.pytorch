USR_DIR=/data/home/GPUAdmin1/asr/deepspeech.pytorch/transformer/
PROBLEM=asr_correction
MODEL=transformer
HPARAMS=transformer_big
DATA_DIR=$HOME/t2t_data
TMP_DIR=/tmp/t2t_datagen
mkdir -p $DATA_DIR $TMP_DIR

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
  --t2t_usr_dir=$USR_DIR


BEAM_SIZE=4
ALPHA=0.6
DECODE_FILE=$DATA_DIR/asr_correction_data_to_decode.txt

echo "hanake hatte allem korperschmuk den einem japanisches medbchen sützhen drücpennd und liegend zeugen muss" >> $DECODE_FILE
#hanake hatte allen körperschmuck den ein japanisches mädchen sitzend trippelnd und liegend zeigen muss
echo "um zulegen göttlichen schönhaiten der fergänglickeit getzil zu werden ie hal war biegsam wie alne reie fel dur" >> $DECODE_FILE
#um zu den göttlichen schönheiten der vergänglichkeit gezählt zu werden ihr hals war biegsam wie eine reiherfeder
echo "ürer aun nur kut wi die flügel eilnes noch nicht fluge sperrerlings so has sie auft der markte und bereite tie iren tieg" >> $DECODE_FILE
#ihre arme kurz wie die flügel eines noch nicht flüggen sperlings sass sie auf der matte und bereitete ihren tee
echo "zu aurbeutetdu sie vorsichtig wie unter eimer glausglocke geng sie abends mit ihrer diemnerin auf dem hohen holzschund zum theautur" >> $DECODE_FILE
#so arbeitete sie vorsichtig wie unter einer glasglocke ging sie abends mit ihrer dienerin auf den hohen holzschuhen zum theater

Inference results INPUT: rer aun nur kut wi die flgel eilnes noch nicht fluge sperrerlings so has sie auft der markte und bereite tie iren tieg
Inference results OUTPUT: ihre arme kurz wie die flügel eines noch nicht flüggen sperlings sass sie auf der matte und bereitete ihren tee

Inference results INPUT: zu aurbeutetdu sie vorsichtig wie unter eimer glausglocke geng sie abends mit ihrer diemnerin auf dem hohen holzschund zum theautur
Inference results OUTPUT: so arbeitete sie vorsichtig wie unter einer glasglocke ging sie abends mit ihrer dienerin auf den hohen holzschuhen zum theater

Inference results INPUT: um zulegen gttlichen schnhaiten der fergnglickeit getzil zu werden ie hal war biegsam wie alne reie fel dur
Inference results OUTPUT: um zu den göttlichen schönheiten der vergänglichkeit gezählt zu werden ihr hals war biegsam wie eine reiherfeder

Inference results INPUT: hanake hatte allem korperschmuk den einem japanisches medbchen stzhen drcpennd und liegend zeugen muss
Inference results OUTPUT: hanake hatte allen körperschmuck den ein japanisches mädchen sitzend trippelnd und liegend zeigen muss

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