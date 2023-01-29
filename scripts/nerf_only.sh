#!/bin/bash

export NERF_PATH=/home/robot-learning/Projects/ScenePose/external/instant-ngp
export VIDEO_PATH=/home/robot-learning/Projects/ScenePose/data/white_cup/white_cup_1

# Run NERF
cd $NERF_PATH
./instant-ngp $VIDEO_PATH