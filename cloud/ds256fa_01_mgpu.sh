TEST_SCRIPT_NAME=ds256fa_01
MODEL=ds256fa

current_date=$(date +%m%d_%H%M)
JOB_NAME=${TEST_SCRIPT_NAME}_${current_date}
JOB_DIR=gs://magnatagatune_dataset/out_$JOB_NAME
TRAIN_FILE=gs://magnatagatune_dataset/train_fbanksdata.tfrecords
EVAL_FILE=gs://magnatagatune_dataset/valid_fbanksdata.tfrecords
METADATA_FILE=gs://magnatagatune_dataset/fbank40_metadata.json

TRAIN_STEPS=55000
LEARNING_RATE=0.01
TRAIN_BATCH=4
EVAL_BATCH=4
REGION=us-east1
CONFIG=config.yaml

gcloud ml-engine jobs submit training $JOB_NAME \
--stream-logs \
--runtime-version 1.2 \
--job-dir $JOB_DIR \
--module-name trainer.task_mgpu \
--package-path trainer/ \
--region $REGION \
--config $CONFIG \
-- \
--train-files $TRAIN_FILE \
--eval-files $EVAL_FILE \
--train-steps $TRAIN_STEPS \
--metadata-files $METADATA_FILE \
--learning-rate $LEARNING_RATE \
--train-batch-size $TRAIN_BATCH \
--eval-batch-size $EVAL_BATCH \
--model-function $MODEL