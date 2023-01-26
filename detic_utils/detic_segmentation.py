import os
import numpy as np


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--detic_path", type=str, required=True)
    parser.add_argument("--dataset", type=str, required=True)
    args = parser.parse_args()

    data_path_full = os.path.join(os.path.dirname(__file__), "../data", args.dataset)
    seg_vis_path = os.path.join(data_path_full, "seg_vis")
    seg_path = os.path.join(data_path_full, "seg")

    # create directories
    if not os.path.exists(seg_vis_path):
        os.makedirs(seg_vis_path)
    if not os.path.exists(seg_path):
        os.makedirs(seg_path)

    image_path = os.path.join(data_path_full, "color")
    image_names = os.listdir(image_path)

    # run detic
    os.system(f"cd " + args.detic_path + 
        f" && python demo_v2.py --config-file {args.detic_path}/configs/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.yaml \
            --input {data_path_full}/color/*.png \
            --output {data_path_full}/seg_vis \
            --seg_output {data_path_full}/seg \
            --attention_bbox_path {data_path_full}/bbox_2d/bbox_2d.txt \
            --vocabulary lvis --opts MODEL.WEIGHTS models/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth")