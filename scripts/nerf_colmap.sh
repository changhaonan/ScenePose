#!/bin/bash

export NERF_PATH=/home/robot-learning/Projects/ScenePose/external/instant-ngp
export VIDEO_PATH=/home/robot-learning/Projects/ScenePose/data/white_cup/white_cup_1

# Prepare data
cd $VIDEO_PATH
python $NERF_PATH/scripts/colmap2nerf.py --video_in $VIDEO_PATH/video.MOV --video_fps 10 --run_colmap --aabb_scale 4

# Run NERF
cd $NERF_PATH
./instant-ngp $VIDEO_PATH