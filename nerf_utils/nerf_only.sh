#!/bin/bash

export NERF_PATH=/home/robot-learning/Projects/ScenePose/external/instant-ngp
export VIDEO_PATH=/home/robot-learning/Projects/ScenePose/data/video_hand

# Run NERF
cd $NERF_PATH
./instant-ngp $VIDEO_PATH