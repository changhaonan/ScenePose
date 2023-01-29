""" Transfer star data to scenepose format
"""
import os


def parse_img_id(img_name):
    return int(img_name.split(".")[0].split("-")[-1])


def trasfer_star2scene_pose(root_path, dataset):
    # prepare path
    star_data_full_path = os.path.join(root_path, "../data", dataset, "star")
    star_data_img_path = os.path.join(star_data_full_path, "cam-00")
    # get image list
    color_save_path = os.path.join(root_path, "../data", dataset, "images")
    depth_save_path = os.path.join(root_path, "../data", dataset, "depth")
    os.makedirs(color_save_path, exist_ok=True)
    os.makedirs(depth_save_path, exist_ok=True)
    # parse image
    img_list = os.listdir(star_data_img_path)
    img_list.sort()
    for img_name in img_list:
        img_idx = parse_img_id(img_name)
        input_full_name = os.path.join(star_data_img_path, img_name)
        if img_name.endswith(".color.png"):
            output_full_name = os.path.join(color_save_path, f"{img_idx + 1}.png")  # use 1-index
            os.system(f"cp {input_full_name} {output_full_name}")
        elif img_name.endswith(".depth.png"):
            output_full_name = os.path.join(depth_save_path, f"{img_idx}.png")
            os.system(f"cp {input_full_name} {output_full_name}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str,
                        default="cracker_box_icg/cracker_box_icg_1")
    args = parser.parse_args()

    # run transfer
    root_path = os.path.dirname(__file__)
    trasfer_star2scene_pose(root_path, args.dataset)
