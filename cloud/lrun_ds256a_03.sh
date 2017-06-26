current_date=$(date +%m%d_%H%M%S)
MODEL=ds256a_t29
JOB_DIR=out_ds256a_01_$current_date
TRAIN_FILE=../magnatagatune/train_rawdata.tfrecords
EVAL_FILE=../magnatagatune/valid_rawdata.tfrecords
METADATA_FILE=../magnatagatune/raw_metadata.json
TRAIN_STEPS=22000
SELECTIVE_TAGS=../magnatagatune/selective_tags.json

gcloud ml-engine local train --package-path trainer \
--module-name trainer.task \
-- \
--train-files $TRAIN_FILE \
--eval-files $EVAL_FILE \
--job-dir $JOB_DIR \
--metadata-files $METADATA_FILE \
--train-steps $TRAIN_STEPS \
--model-function $MODEL \
--selective-tags $SELECTIVE_TAGS