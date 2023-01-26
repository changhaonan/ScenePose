#!/bin/bash

# Prepare data
export DATASET_PATH="/home/robot-learning/Projects/ScenePose/data"
export DATA_NAME="video_dragon"
python data_prepare.py --src_path=$DATASET_PATH/$DATA_NAME --dst_path=$DATASET_PATH/$DATA_NAME --src_path="mov" --fps=5

# Run COLMAP sparse reconstruction
colmap feature_extractor \
    --database_path $DATASET_PATH/$DATA_NAME/database.db \
    --image_path $DATASET_PATH/$DATA_NAME/images

colmap exhaustive_matcher \
    --database_path $DATASET_PATH/$DATA_NAME/database.db

mkdir $DATASET_PATH/$DATA_NAME/sparse

colmap mapper \
    --database_path $DATASET_PATH/$DATA_NAME/database.db \
    --image_path $DATASET_PATH/$DATA_NAME/images \
    --output_path $DATASET_PATH/$DATA_NAME/sparse
