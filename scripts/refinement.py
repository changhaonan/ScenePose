import cv2
import time
import matplotlib.pyplot as plt
import segmentation_refinement as refine
import os
from tqdm import tqdm
import numpy as np


if __name__ == "__main__":
    # parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="data/video_dragon")
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--L", type=int, default=900)
    parser.add_argument("--device", type=str, default="cuda:0")
    args = parser.parse_args()

    # load image and mask
    image_path = os.path.join(args.data_path, "images")
    seg_path = os.path.join(args.data_path, "seg")
    refine_path = os.path.join(args.data_path, "mask")
    if not os.path.exists(refine_path):
        os.makedirs(refine_path)

    # model_path can also be specified here
    # This step takes some time to load the model
    # build refiner
    refiner = refine.Refiner(device="cuda:0")  # device can also be "cpu"

    # Count number of images
    num_images = len(os.listdir(image_path))
    for image_idx in tqdm(range(1, num_images + 1)):
        image_file = os.path.join(image_path, "{:04d}.jpg".format(image_idx))
        image = cv2.imread(image_file)
        mask_file = os.path.join(seg_path, "{:04d}.png".format(image_idx))
        mask = cv2.imread(mask_file, cv2.IMREAD_UNCHANGED)
        # Generate a grayscale mask from each mask
        label_list = np.unique(mask)
        for label in label_list:
            if label != 0:
                label_mask = np.zeros(mask.shape, dtype=np.uint8)
                label_mask[mask == label] = 255
                # Fast - Global step only.
                # Smaller L -> Less memory usage; faster in fast mode.
                output = refiner.refine(image, label_mask, fast=False, L=900)
                # Use threshold to get binary mask
                threshold = 10
                output[output < threshold] = 0
                output[output >= threshold] = 255
                # this line to save output
                cv2.imwrite(os.path.join(refine_path, f"{image_idx:04}_{label:04}.jpg"), label_mask)
