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
    pytracking_path = "/home/robot-learning/Projects/pytracking/pytracking"
    tracker_name = "tomp"
    tracker_param = "tomp50"
    data_set = "cracker_box/cracker_box_3"
    video_path = os.path.join(os.path.dirname(__file__), "../data", data_set, "color/%d.png")
    output_path = os.path.join(os.path.dirname(__file__), "../data", data_set, "bbox_2d")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    run_2d_tracker(tracker_name, tracker_param, video_path, pytracking_path, output_path)
