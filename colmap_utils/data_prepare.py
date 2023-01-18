import os
import sys
import cv2
from tqdm import tqdm


def data_prepare_general(src_path, dst_path, src_type, other_args):
    print("Start data preparation...")
    if src_type == "icra23":
        data_prepare_icra23(src_path, dst_path)
    elif src_type == "mov":
        data_prepare_mov(src_path, dst_path, other_args.fps)
    else:
        raise ValueError("Unknown src_type: {}".format(src_type))


def data_prepare_icra23(src_path, dst_path):
    # Copy images
    src_image_path = os.path.join(src_path, "color")
    dst_image_path = os.path.join(dst_path, "images")
    # Create dst_image_path
    if not os.path.exists(dst_image_path):
        os.makedirs(dst_image_path)
    # Count number of images
    num_images = len(os.listdir(src_image_path))
    for image_idx in tqdm(range(num_images)):
        src_image_file = os.path.join(
            src_image_path, "{:04d}-color.png".format(image_idx))
        dst_image_file = os.path.join(
            dst_image_path, f"image{image_idx}.jpg")
        image = cv2.imread(src_image_file)
        cv2.imwrite(dst_image_file, image)


def data_prepare_mov(src_path, dst_path, fps=5):
    video_file = os.path.join(src_path, "video.MOV")
    dst_image_path = os.path.join(dst_path, "images")
    # Create dst_image_path
    if not os.path.exists(dst_image_path):
        os.makedirs(dst_image_path)
    # using ffmpeg to extract images
    os.system(
        f"ffmpeg -i {video_file} -vf fps={fps} {dst_image_path}/image%d.jpg")


if __name__ == "__main__":
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_path", type=str, required=True)
    parser.add_argument("--dst_path", type=str, default="./data")
    parser.add_argument("--src_type", type=str, default="icra23")
    parser.add_argument("--fps", type=int, default=5)
    args = parser.parse_args()
    data_prepare_general(args.src_path, args.dst_path, args.src_type, args)
