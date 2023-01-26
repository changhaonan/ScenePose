#! /bin/bash

export DETIC_PATH=/home/robot-learning/Projects/ScenePose/external/Detic
export SRC_PATH=/home/robot-learning/Projects/ScenePose/data/mastard_bottle/mastard_bottle_1

# Build export folder if not exist
mkdir -p $SRC_PATH/seg_vis
mkdir -p $SRC_PATH/seg

cd $DETIC_PATH
# Go through all images
for f in $SRC_PATH/color/*.png; do
    # Get the filename without extension
    filename=$(basename -- "$f")
    filename="${filename%.*}"
    # Log info
    echo "Processing $filename"
    # Run Detic
    python demo_v2.py --config-file $DETIC_PATH/configs/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.yaml \
        --input $SRC_PATH/color/$filename.png \
        --output $SRC_PATH/seg_vis/$filename.jpg \
        --seg_output $SRC_PATH/seg/$filename.png \
        --attention_bbox_path $SRC_PATH/bbox_2d/bbox_2d.txt \
        --vocabulary lvis --opts MODEL.WEIGHTS models/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth
done
