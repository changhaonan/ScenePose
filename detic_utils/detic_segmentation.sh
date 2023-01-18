#! /bin/bash

export DETIC_PATH=/home/robot-learning/Projects/ScenePose/external/Detic
export SRC_PATH=/home/robot-learning/Projects/ScenePose/data/video_dragon

cd $DETIC_PATH
# Go through all images
for f in $SRC_PATH/images/*.jpg; do
    # Get the filename without extension
    filename=$(basename -- "$f")
    filename="${filename%.*}"
    # Log info
    echo "Processing $filename"
    # Run Detic
    python demo.py --config-file $DETIC_PATH/configs/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.yaml \
        --input $SRC_PATH/images/$filename.jpg --output $SRC_PATH/segmentation/$filename.jpg \
        --vocabulary lvis --opts MODEL.WEIGHTS models/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth
done
