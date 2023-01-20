import easy3d_viewer as easy3d
import numpy as np
import os


def read_pose(pose_file):
    pose = np.loadtxt(pose_file).astype(np.float32)
    return pose

if __name__ == "__main__":
    # read poses
    pose_dir = "/home/robot-learning/Projects/ScenePose/external/OnePose/data/onepose_datasets/sample_data/0501-matchafranzzi-box/matchafranzzi-1/poses_ba"
    pose_files = [pose_dir + "/" + f for f in os.listdir(pose_dir)]
    pose_files.sort()
    poses = [read_pose(pose_file) for pose_file in pose_files]
    # save them into context
    experiment_name = "one_pose"
    output_dir = "/home/robot-learning/Projects/ScenePose/external/Easy3DViewer/public/test_data"
    context = easy3d.Context()
    context.setDir(os.path.join(output_dir, experiment_name))

    for i in range(len(poses)):
        context.open(i)
        context.addCoord("cam", "", poses[i], 0.01)
        context.addCoord("origin", "", np.eye(4, dtype=np.float32), 0.01)
        context.close()