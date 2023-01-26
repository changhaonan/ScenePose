import easy3d_viewer as easy3d
import open3d as o3d
from open3d.visualization import draw_geometries
import os
import numpy as np
from scipy.spatial.transform import Rotation as R


def load_camera_txt(camera_path):
    # read txt file
    with open(camera_path, "r") as f:
        lines = f.readlines()
    # parse camera info
    camera_poses = {}
    line_jump = True
    flip_matrix = np.array([
        [1, 0, 0, 0], 
        [0, -1, 0, 0], 
        [0, 0, -1, 0], 
        [0, 0, 0, 1]
    ])
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        # flip the jump flag
        line_jump = not line_jump
        if line_jump:
            continue
        line = line.split(" ")
        camera_id = int(line[0]) - 1  # 1-indexed to 0-indexed
        quat = np.array([float(line[2]), float(line[3]), float(line[4]), float(line[1])])
        trans = np.array([float(line[5]), float(line[6]), float(line[7])])
        camera_T = np.eye(4)
        camera_T[:3, :3] = R.from_quat(quat).as_matrix()
        camera_T[:3, 3:] = trans[:, np.newaxis]
        camera_T = np.linalg.inv(camera_T)
        camera_poses[camera_id] = camera_T
    return camera_poses


def load_3d_box(corners3D_path):
    # read txt file
    with open(corners3D_path, "r") as f:
        lines = f.readlines()
    corners3D = []
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        line = line.split(" ")
        corners3D.append([float(line[0]), float(line[1]), float(line[2])])
    # transform corners3D to visualize format
    corners3D = np.array(corners3D)
    # lines span from points 0 to 1, 1 to 2, 2 to 3, etc...
    lines = [[0, 1], [1, 2], [2, 3], [0, 3],
            [4, 5], [5, 6], [6, 7], [4, 7],
            [0, 4], [1, 5], [2, 6], [3, 7]]

    # use the same color for all lines
    colors = [[0, 1, 0] for _ in range(len(lines))]

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(corners3D)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)
    return line_set


def load_points3D_txt(points3D_path):
    """
    Load points3D.txt file into open3d point cloud
    @param points3D_path: path to points3D.txt
    @return: open3d point cloud
    """
    # read txt file
    with open(points3D_path, "r") as f:
        lines = f.readlines()
    # parse camera info
    points_position = []
    points_rgb = []
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        line = line.split(" ")
        xyz = np.array([float(line[1]), float(line[2]), float(line[3])])  # flip y and z
        rgb = np.array([float(line[4]), float(line[5]), float(line[6])])
        points_position.append(xyz)
        points_rgb.append(rgb)
    
    # wrap into open3d point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.stack(points_position))
    pcd.colors = o3d.utility.Vector3dVector(np.stack(points_rgb) / 255.0)
    return pcd


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--colmap_model_dir", type=str, default="/home/robot-learning/Projects/ScenePose/data/mastard_bottle/mastard_bottle_1/colmap_text")
    args = parser.parse_args()

    # load info
    camera_poses = load_camera_txt(os.path.join(args.colmap_model_dir + "/images.txt"))
    features_3d = load_points3D_txt(os.path.join(args.colmap_model_dir + "/points3D.txt"))
    # create open3d bbox
    bbox = load_3d_box(os.path.join(args.colmap_model_dir + "/../../box3d_corners.txt"))
    # visualize 
    # create camera vis
    camera_vis = []
    for camera_id, camera_T in camera_poses.items():
        camera = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.2, origin=[0, 0, 0])
        camera.transform(camera_T)
        camera_vis.append(camera)
    origin = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
    draw_geometries([features_3d] + camera_vis + [origin] + [bbox])