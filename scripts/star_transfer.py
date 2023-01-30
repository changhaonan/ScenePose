""" Transfer star data to scenepose format
"""
import os
import json


def parse_img_id(img_name):
    return int(img_name.split(".")[0].split("-")[-1])


def trasfer_star2scene_pose(root_path, dataset):
    # prepare path
    star_data_full_path = os.path.join(root_path, "../data", dataset, "star")
    star_data_img_path = os.path.join(star_data_full_path, "cam-00")
    # get image list
    data_save_path = os.path.join(root_path, "../data", dataset)
    color_save_path = os.path.join(root_path, "../data", dataset, "images")
    depth_save_path = os.path.join(root_path, "../data", dataset, "depth")
    os.makedirs(color_save_path, exist_ok=True)
    os.makedirs(depth_save_path, exist_ok=True)

    # parse context
    context_json = json.load(
        open(os.path.join(star_data_full_path, "context.json")))
    intrinsic = context_json["cam-00"]["intrinsic"]
    # save intrinsic to intrinsics.txt
    with open(os.path.join(data_save_path, "intrinsics.txt"), "w") as f:
        f.writelines(
            [
                f"fx: {intrinsic[0]}\n",
                f"fy: {intrinsic[1]}\n",
                f"cx: {intrinsic[2]}\n",
                f"cy: {intrinsic[3]}",
            ]
        )

    # parse image
    img_list = os.listdir(star_data_img_path)
    img_list.sort()
    for img_name in img_list:
        img_idx = parse_img_id(img_name)
        input_full_name = os.path.join(star_data_img_path, img_name)
        if img_name.endswith(".color.png"):
            output_full_name = os.path.join(
                color_save_path, f"{img_idx + 1}.png")  # use 1-index
            os.system(f"cp {input_full_name} {output_full_name}")
        elif img_name.endswith(".depth.png"):
            output_full_name = os.path.join(depth_save_path, f"{img_idx}.png")
            os.system(f"cp {input_full_name} {output_full_name}")


def trasfer_star2reconstruct(root_path, dataset):
    # prepare path
    star_data_full_path = os.path.join(root_path, "../data", dataset, "star")
    star_data_img_path = os.path.join(star_data_full_path, "cam-00")
    # get image list
    data_save_path = os.path.join(root_path, "../data", dataset, "reconstruct")
    color_save_path = os.path.join(root_path, "../data", dataset, "reconstruct", "images")
    depth_save_path = os.path.join(root_path, "../data", dataset, "reconstruct", "depth")
    os.makedirs(data_save_path, exist_ok=True)
    os.makedirs(color_save_path, exist_ok=True)
    os.makedirs(depth_save_path, exist_ok=True)
    
    # parse context and save it to config.json
    context_json = json.load(
        open(os.path.join(star_data_full_path, "context.json")))
    intrinsic = context_json["cam-00"]["intrinsic"]
    width = context_json["cam-00"]["image_cols"]
    height = context_json["cam-00"]["image_rows"]
    output_config = {
        "im_w": width,
        "im_h": height,
        "depth_scale": 1000,
        "cam_intr": [
            [
                intrinsic[0], 0, intrinsic[2]
            ],
            [
                0, intrinsic[1], intrinsic[3]
            ],
            [
                0, 0, 1
            ]
        ]
    }
    with open(os.path.join(data_save_path, "config.json"), "w") as f:
        json.dump(output_config, f, indent=4)

    # parse image
    img_list = os.listdir(star_data_img_path)
    img_list.sort()
    for img_name in img_list:
        img_idx = parse_img_id(img_name)
        input_full_name = os.path.join(star_data_img_path, img_name)
        if img_name.endswith(".color.png"):
            output_full_name = os.path.join(
                color_save_path, f"{img_idx :04}.color.png")  # use 1-index
            os.system(f"cp {input_full_name} {output_full_name}")
        elif img_name.endswith(".depth.png"):
            output_full_name = os.path.join(depth_save_path, f"{img_idx :04}.depth.png")
            os.system(f"cp {input_full_name} {output_full_name}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str,
                        default="cracker_box_icg/cracker_box_icg_1")
    # scene_pose, reconstruction
    parser.add_argument("--mode", type=str, default="scene_pose")
    args = parser.parse_args()

    # run transfer
    root_path = os.path.dirname(__file__)
    if args.mode == "scene_pose":
        trasfer_star2scene_pose(root_path, args.dataset)
    elif args.mode == "reconstruct":
        trasfer_star2reconstruct(root_path, args.dataset)
