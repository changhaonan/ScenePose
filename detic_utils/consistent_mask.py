"""
Generate consistent mask using 2D tracker and Detic
"""
import os


def run_2d_tracker(tracker_name, tracker_param, video_path, pytracking_path, output_path):
    """
    Run 2D tracker
    """
    os.system(f"python run_video.py {tracker_name} {tracker_param} {video_path} --save_results")
    # copy results to output path
    os.system(f"cp {pytracking_path}/tracking_results/{tracker_name}/{tracker_param}/video_%d.txt {output_path}/bbox_2d.txt")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracker_name", type=str, default="tomp")
    parser.add_argument("--tracker_param", type=str, default="tomp50")
    parser.add_argument("--dataset", type=str, default="mastard_bottle/mastard_bottle_1")
    parser.add_argument("--pytracking_path", type=str, default="/home/robot-learning/Projects/pytracking/pytracking")
    args = parser.parse_args()

    video_path = os.path.join(os.path.dirname(__file__), f"../data/{args.dataset}/color/%d.png")
    output_path = os.path.join(os.path.dirname(__file__), f"../data/{args.dataset}/bbox_2d")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    run_2d_tracker(args.tracker_name, args.tracker_param, video_path, args.pytracking_path, output_path)
