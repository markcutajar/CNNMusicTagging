MODEL=dielemanschrauwen256
JOB_NAME=ds256_08
JOB_DIR=gs://magnatagatune_dataset/output_ds256_08
TRAIN_FILE=gs://magnatagatune_dataset/train_rawdata.tfrecords
EVAL_FILE=gs://magnatagatune_dataset/valid_rawdata.tfrecords
METADATA_FILE=gs://magnatagatune_dataset/raw_metadata.json
TRAIN_STEPS=22000
REGION=us-east1
CONFIG=config.yaml
WINDOW_SIZE=51776
#SELTAGS=gs://magnatagatune_dataset/selective_tags.json