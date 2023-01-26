import os
import json
import numpy as np
import cv2

def prepare_colmap_by_nerf(video_path, nerf_path, fps=10, aabb_scale=4):
    os.chdir(video_path)
    os.system(f"python {nerf_path}/scripts/colmap2nerf.py --keep_colmap_coords --video_in video.MOV --video_fps {fps} --run_colmap --aabb_scale {aabb_scale}")
    # copy images to color folder
    copy_image_to_onepose(video_path)


def copy_image_to_onepose(data_path):
    # copy images
    input_path = os.path.join(data_path, "images")
    output_path = os.path.join(data_path, "color")
    output_2_path = os.path.join(data_path, "color_full")
    # copy all images to color folder and transfer from jpg to png
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        os.makedirs(output_2_path)
    else:
        os.system(f"rm -rf {output_path}")
        os.system(f"rm -rf {output_2_path}")
        os.makedirs(output_path)
        os.makedirs(output_2_path)
    for image_file in os.listdir(input_path):
        full_image_file = os.path.join(input_path, image_file)
        image = cv2.imread(full_image_file)
        # nerf is 1-indexed, and one-pose is 0-indexed
        png_image_file = f"{int(image_file.split('.')[0]) - 1}.png"
        cv2.imwrite(os.path.join(output_path, png_image_file), image)
        cv2.imwrite(os.path.join(output_2_path, png_image_file), image)
    # copy video from video.MOV to Frames.m4v
    in_video_file = os.path.join(data_path, "video.MOV")
    out_video_file = os.path.join(data_path, "Frames.m4v")
    os.system(f"ffmpeg -i {in_video_file} -vcodec libx264 {out_video_file}")


def transfer_camera_to_onepose(data_path):
    camera_T_file = os.path.join(data_path, "transforms.json")
    camera_T_json = json.load(open(camera_T_file, "r"))

    intrin_path = os.path.join(data_path, "intrin_ba")
    if not os.path.exists(intrin_path):
        os.makedirs(intrin_path)
    extrin_path = os.path.join(data_path, "poses_ba")
    if not os.path.exists(extrin_path):
        os.makedirs(extrin_path)
    
    # parse intrinsic
    fx = camera_T_json["fl_x"]
    fy = camera_T_json["fl_y"]
    cx = camera_T_json["cx"]
    cy = camera_T_json["cy"]
    width = camera_T_json["w"]
    height = camera_T_json["h"]
    intrin = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

    # write extrinsic ba
    for frame in camera_T_json["frames"]:
        file_path = frame["file_path"]
        i = int(file_path.split(".")[-2].split("/")[-1]) - 1  # nerf is 1-indexed, and one-pose is 0-indexed
        frame_T = np.array(frame["transform_matrix"])
        frame_T = np.linalg.inv(frame_T)
        flip_mat = np.array([
			[1, 0, 0, 0],
			[0, -1, 0, 0],
			[0, 0, -1, 0],
			[0, 0, 0, 1]
		])
        frame_T = np.matmul(flip_mat, frame_T)  # colmap representation is different from nerf
        extrin_file = os.path.join(extrin_path, f"{i}.txt")
        np.savetxt(extrin_file, frame_T)  # one-pose is using object pose

        intrin_file = os.path.join(intrin_path, f"{i}.txt")
        np.savetxt(intrin_file, intrin)

    # write intrinsic
    intrin_file = os.path.join(data_path, "intrinsics.txt")
    fo = open(intrin_file, "w")
    fo.write(f"fx: {fx}\n")
    fo.write(f"fy: {fy}\n")
    fo.write(f"cx: {cx}\n")
    fo.write(f"cy: {cy}\n")
    fo.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="data/video_dragon_op/video_dragon_op_1")
    parser.add_argument("--nerf_path", type=str, required=True)
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--aabb_scale", type=int, default=4)
    parser.add_argument("--redo_sfm", action="store_true")
    args = parser.parse_args()

    # Run colmap first to get a camera poses
    video_path = args.dataset
    nerf_path = args.nerf_path
    if args.redo_sfm:
        prepare_colmap_by_nerf(video_path, nerf_path, fps=args.fps, aabb_scale=args.aabb_scale)

    transfer_camera_to_onepose(video_path)