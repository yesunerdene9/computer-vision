import os
import json
import time

import numpy as np
import pandas as pd
import open3d as o3d
import seaborn as sns
import matplotlib.pyplot as plt
import optitrack.csv_reader as csv

from optitrack.geometry import *


#--- COLORS FOR THE PLOT ---#
COLOR_GREEN = "#308868"
COLOR_RED_1 = "#EC2F74"
COLOR_RED_2 = "#622DB1"
COLOR_GREEN_2 = "#14CE23"
COLOR_RED_1_2 = "#D729A9"


#--- JOINTS ---#
body_edges_no_fingers = [
        [0, 1],  # Hip → Ab
        [1, 2],  # Ab → Chest
        [2, 3],  # Chest → Neck
        [3, 4],  # Neck → Head
        [3, 5],  # Neck → LShoulder
        [5, 6],  # LShoulder → LUArm
        [6, 7],  # LUArm → LFArm
        [7, 8],  # LFArm → LHand
        [3, 9],  # Neck → RShoulder
        [9, 10], # RShoulder → RUArm
        [10, 11],# RUArm → RFArm
        [11, 12],# RFArm → RHand
        [0, 13], # Hip → LThigh
        [13, 14],# LThigh → LShin
        [14, 15],# LShin → LFoot
        [15, 16],# LFoot → LToe
        [0, 17], # Hip → RThigh
        [17, 18],# RThigh → RShin
        [18, 19],# RShin → RFoot
        [19, 20] # RFoot → RToe
    ]

body_edges = [
        # Upper body
        [0, 1],  # Hip → Ab
        [1, 2],  # Ab → Chest
        [2, 3],  # Chest → Neck
        [3, 4],  # Neck → Head
    
        [3, 5],  # Neck → LShoulder
        [5, 6],  # LShoulder → LUArm
        [6, 7],  # LUArm → LFArm
        [7, 8],  # LFArm → LHand
        [3, 24],  # Neck → RShoulder
        [24, 25], # RShoulder → RUArm
        [25, 26],# RUArm → RFArm
        [26, 27],# RFArm → RHand

        # Lower body
        [0, 43], # Hip → LThigh
        [43, 44],# LThigh → LShin
        [44, 45],# LShin → LFoot
        [45, 46],# LFoot → LToe
        [0, 47], # Hip → RThigh
        [47, 48],# RThigh → RShin
        [48, 49],# RShin → RFoot
        [49, 50], # RFoot → RToe

        # Left Hand fingers
        [8, 9],  # LHand → LThumb1
        [9, 10], # LThumb1 → LThumb2
        [10, 11],  # LThumb2 → LThumb3
        [8, 12],  # LHand → LIndex1
        [12, 13],  # LIndex1 → LIndex2
        [13, 14], # LIndex2 → LIndex3
        [8, 15],  # LHand → LMiddle1
        [15, 16],  # LMiddle1 → LMiddle2
        [16, 17], # LMiddle2 → LMiddle3
        [8, 18],  # LHand → LRing1
        [18, 19],  # LRing1 → LRing2
        [19, 20], # LRing2 → LRing3
        [8, 21],  # LHand → LPinky1
        [21, 22],  # LPinky1 → LPinky2
        [22, 23], # LPinky2 → LPinky3

        # Right Hand fingers
        [27, 28],  # RHand → RThumb1
        [28, 29], # RThumb1 → RThumb2
        [29, 30],  # RThumb2 → RThumb3
        [27, 31],  # RHand → RIndex1
        [31, 32],  # RIndex1 → RIndex2
        [32, 33], # RIndex2 → RIndex3
        [27, 34],  # RHand → RMiddle1
        [34, 35],  # RMiddle1 → RMiddle2
        [35, 36], # RMiddle2 → RMiddle3
        [27, 37],  # RHand → RRing1
        [37, 38],  # RRing1 → RRing2
        [38, 30], # RRing2 → RRing3
        [27, 40],  # RHand → RPinky1
        [40, 41],  # RPinky1 → RPinky2
        [41, 42], # RPinky2 → RPinky3
    ]



#--- CALCULATION FUNCTIONS ---#

def calculate_hip_drop(bones_pos):
    """
        Extracts drop value over the frames for hips
        
        Parameters:
            bone_pos: bone positions over the frames
        
        Returns:
            drops: dictionary with the hip drops and the frames
    """

    drops = []

    for frame_idx, joints in enumerate(bones_pos):

        # Y-coordinate value of the LThigh position     joints[43][1]
        # Y-coordinate value of the RThigh position     joints[47][1]
        hips_drop = joints[43][1] - joints[47][1]

        drops.append({
            "frame": frame_idx,
            "hips_drop": hips_drop,
        })
    return drops


def calculate_angle(v1, v2):
    """
        Calculates the angle between two vectors
    """
    v1_norm = np.linalg.norm(v1)
    v2_norm = np.linalg.norm(v2)

    # if vectors are 0, angle is 0
    if v1_norm == 0 or v2_norm == 0:
        return 0.0  

    dot_product = np.dot(v1, v2)

    cos_theta = np.clip(dot_product / (v1_norm * v2_norm), -1.0, 1.0)
    angle_rad = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_rad)
    
    return angle_deg


def calculate_angles(bones_pos):
    """
        Extracts the angle over the frames for specific areas
        
        Parameters:
            bone_pos: bone positions over the frames
        
        Returns:
            angles: dictionary with the angles and the frames
    """

    angles = []

    for frame_idx, joints in enumerate(bones_pos):
        # Vector    LUArm → LShoulder      (joints[5] - joints[6])
        # Vector    LUArm → LFArm          (joints[7] - joints[6])
        shoulder_angle = calculate_angle(joints[5] - joints[6], joints[7] - joints[6])

        # Vector    Rthigh → LThigh        (joints[3] - joints[5])
        # Vector    Rthigh → LThigh        (joints[6] - joints[5])       straight forward in X
        hips_angle = calculate_angle(joints[3] - joints[5], joints[6] - joints[5])

        # Vector    Rthigh → LThigh        (joints[47] - joints[43]) 
        # Vector    Horizontal plane        (np.array([1, 0, 0])          straight upward in Y
        hips_raise_angle = calculate_angle(joints[47] - joints[43], np.array([1, 0, 0]))

        # Vector    Hip → Neck             (joints[3] - joints[0]) 
        # Vector    Vertical plane          np.array([0, 1, 0])
        spine_tilt_angle = calculate_angle(joints[3] - joints[0], np.array([0, 1, 0]))

        # Vector    RFoot → RThigh          (joints[47] - joints[49]) 
        # Vector    Vertical plane          np.array([0, 1, 0])
        leg_tilt_angle = calculate_angle(joints[47] - joints[49], np.array([0, 1, 0]))

        angles.append({
            "frame": frame_idx,

            "shoulder": shoulder_angle,
            "hips": hips_angle,
            "hips_raise": hips_raise_angle,
            "spine_tilt": spine_tilt_angle,
            "leg_tilt": leg_tilt_angle
        })
    
    return angles


def calculate_distance(p1, v2):
    """
        Calculate Euclidean distance between two physical positions (for feet and toes)
        
        Parameters:
            p1, p2: Arrays or lists representing positions ([X, Y, Z])
        
        Returns:
            float: Distance between the two positions
    """

    # Euclidean distance
    distance_mm = np.linalg.norm(np.array(p1) - np.array(v2))

    # Convert mm → cm (Recording Length Units is in Millimeters)
    distance_cm = distance_mm / 10

    return distance_cm


def calculate_distances(bones_pos):
    """
        Calculates the distance between feet and tow over the frame
        
        Parameters:
            bone_pos: bone positions over the frames
        
        Returns:
            angles: dictionary with the distances and the frames
    """

    distances = []

    for frame_idx, joints in enumerate(bones_pos):

        # 3D position of the RToe and LToe     joints[46], joints[50]
        toe_distance = calculate_distance(joints[46], joints[50])

        # 3D position of the RFeet and LFeet     joints[45], joints[49]
        feet_distance = calculate_distance(joints[45], joints[49])

        distances.append({
            "frame": frame_idx,
            "toe": toe_distance,
            "feet": feet_distance
        })

    return distances


def analyze_metric_series(metrics, key):
    """
        Analyze a time series of metrics, returning statistics.
        
        Parameters:
            metrics: List or 1D np.array of metric values
        
        Returns:
            stats: statistics of the metrics
    """

    metric_data = np.array([frame[key] for frame in metrics])

    stats = {
        "mean": np.mean(metric_data),
        "std": np.std(metric_data),
        "min": np.min(metric_data),
        "max": np.max(metric_data),
        "range": np.ptp(metric_data),
    }

    return stats



#--- PLOTTING FUNCTIONS ---#

def plot_metric_over_time(
        metrics1, metrics2, metrics3, 
        title, label1, label2, label3, ylabel, 
        key, output_file, show_plots):
    """
        Shows a plot of the metric over time.
    """
    
    df1 = pd.DataFrame(metrics1)
    df1['label'] = label1

    df2 = pd.DataFrame(metrics2)
    df2['label'] = label2

    if metrics3 is not None:
        df3 = pd.DataFrame(metrics3)
        df3['label'] = label3
        df = pd.concat([df1, df2, df3], ignore_index=True)
        custom_palette =  {label1: COLOR_GREEN, label2: COLOR_RED_1, label3: COLOR_RED_2}
    else:
        df = pd.concat([df1, df2], ignore_index=True)
        custom_palette = {label1: COLOR_GREEN, label2: COLOR_RED_1}

    sns.set(style='whitegrid', palette='muted', font_scale=1.1)

    plt.figure(figsize=(14, 8))

    sns.lineplot(data=df, x='frame', y=key, hue='label', linewidth=1.5, palette=custom_palette)

    plt.title(title, fontsize=16)
    plt.xlabel('Frame')
    plt.ylabel(ylabel)
    plt.legend(title='Type', loc='best')
    plt.tight_layout()

    plt.savefig(output_file)
    if show_plots:
        plt.show()

    plt.close()


def plot_distribution(metrics1, metrics2, metrics3, 
                      title, label1, label2, label3, xlabel, 
                      key, output_file, show_plots):
    """
        Show a plot of distribution of the metric over time.
    """

    df_1 = pd.DataFrame(metrics1)
    df_2 = pd.DataFrame(metrics2)

    if metrics3 is not None:
        df_3 = pd.DataFrame(metrics3)

    plt.figure(figsize=(14, 8))
    
    sns.histplot(df_1[key], bins=50, stat="density", color=COLOR_GREEN, label=label1, element="step", fill=True, alpha=0.3)
    sns.kdeplot(df_1[key], fill=False, color=COLOR_GREEN, alpha=0.8)

    sns.histplot(df_2[key], bins=50, stat="density", color=COLOR_RED_1, label=label2, element="step", fill=True, alpha=0.3)
    sns.kdeplot(df_2[key], fill=False, color=COLOR_RED_1, alpha=0.8)

    if metrics3 is not None:
        sns.histplot(df_3[key], bins=50, stat="density", color=COLOR_RED_2, label=label3, element="step", fill=True, alpha=0.3)
        sns.kdeplot(df_3[key], fill=False, color=COLOR_RED_2, alpha=0.8)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_file)
    if show_plots:
        plt.show()

    plt.close()
    

def plot_combined_time_and_distribution(metrics1, metrics2, metrics3,
                                        title_time, title_dist,
                                        label1, label2, label3, label4,
                                        ylabel, xlabel, key, key2, output_file, show_plots):
    """
        Save and show a plot of the metric over time and ditribution.
    """

    df1 = pd.DataFrame(metrics1)
    df1['label'] = label1

    df2 = pd.DataFrame(metrics2)
    df2['label'] = label2

    if metrics3 is not None:
        df3 = pd.DataFrame(metrics3)
        df3['label'] = label3
        df = pd.concat([df1, df2, df3], ignore_index=True)
        palette = {label1: COLOR_GREEN, label2: COLOR_RED_1, label3: COLOR_RED_2}

    else:
        df = pd.concat([df1, df2], ignore_index=True)
        palette = {label1: COLOR_GREEN, label2: COLOR_RED_1}

        if key2 is not None:
            df3 = pd.DataFrame(metrics1)
            df3['label'] = label3
            df4 = pd.DataFrame(metrics2)
            df4['label'] = label4

            df_2 =  pd.concat([df3, df4], ignore_index=True)
            palette = {label1: COLOR_GREEN, label2: COLOR_RED_1, label3: COLOR_GREEN_2, label4: COLOR_RED_1_2}

    sns.set(style='whitegrid', font_scale=1.1)
    fig, axs = plt.subplots(1, 2, figsize=(18, 8))

    # --- Left: Time Series ---
    sns.lineplot(data=df, x='frame', y=key, hue='label', palette=palette, linewidth=1.8, ax=axs[0])
    if key2 is not None:
        sns.lineplot(data=df_2, x='frame', y=key2, hue='label', palette=palette, linewidth=1.8, ax=axs[0])

    axs[0].set_title(title_time)
    axs[0].set_xlabel('Frame')
    axs[0].set_ylabel(ylabel)
    axs[0].legend(title='Type')

    # --- Right: Histogram + KDE ---
    sns.histplot(df1[key], bins=50, stat="density", color=COLOR_GREEN, label=label1, ax=axs[1], element="step", fill=True, alpha=0.3)
    sns.kdeplot(df1[key], color=COLOR_GREEN, ax=axs[1], fill=False, alpha=0.8)

    sns.histplot(df2[key], bins=50, stat="density", color=COLOR_RED_1, label=label2, ax=axs[1], element="step", fill=True, alpha=0.3)
    sns.kdeplot(df2[key], color=COLOR_RED_1, ax=axs[1], fill=False, alpha=0.8)

    if metrics3 is not None:
        sns.histplot(df3[key], bins=50, stat="density", color=COLOR_RED_2, label=label3, ax=axs[1], element="step", fill=True, alpha=0.3)
        sns.kdeplot(df3[key], color=COLOR_RED_2, ax=axs[1], fill=False, alpha=0.8)

    if key2 is not None:
        sns.histplot(df1[key2], bins=50, stat="density", color=COLOR_GREEN_2, label=label3, ax=axs[1], element="step", fill=True, alpha=0.3)
        sns.kdeplot(df1[key2], color=COLOR_GREEN_2, ax=axs[1], fill=False, alpha=0.8)

        sns.histplot(df2[key2], bins=50, stat="density", color=COLOR_RED_1_2, label=label4, ax=axs[1], element="step", fill=True, alpha=0.3)
        sns.kdeplot(df2[key2], color=COLOR_RED_1_2, ax=axs[1], fill=False, alpha=0.8)

    axs[1].set_title(title_dist)
    axs[1].set_xlabel(xlabel)
    axs[1].set_ylabel('Density')
    axs[1].legend(title='Type')

    plt.tight_layout()
    plt.savefig(output_file)
    if show_plots:
        plt.show()
    plt.close()



#--- SUPPORTING FUNCTIONS ---#

def interpolate_bones_positions(bones_pos):
    """
    Interpolate invalid frames
    """
    interpolated_bones = bones_pos.copy()
    num_frames, num_joints, _ = bones_pos.shape

    for joint in range(num_joints):
        invalid_frames = (bones_pos[:, joint] == 0).all(axis=1) #find invalid (=0,0,0) frames
        
        for dim in range(3): #3=x,y,z
            joint_coord = bones_pos[:, joint, dim]  #extract the value for the current joint and dimension

            if np.any(invalid_frames):
                valid_mask = ~invalid_frames        #~ è operatore NOT che agisce su array
                if np.any(valid_mask):
                    valid_indices = np.where(valid_mask)[0]
                    invalid_indices = np.where(invalid_frames)[0]

                    # NumPy's interpolation function
                    joint_coord[invalid_frames] = np.interp(
                        invalid_indices,
                        valid_indices,
                        joint_coord[valid_mask]
                    )
            
            # Update the interpolated_bones array for the current dimension
            interpolated_bones[:, joint, dim] = joint_coord

    return interpolated_bones


def get_bones_position(file):
    """
    Get the bones positions from the loaded csv file from the mocap.
    """
    bodies = file.rigid_bodies

    bones_pos = []
    if len(bodies) > 0:
        for body in bodies: 
            bones = file.rigid_bodies[body]
            
            # set 0,0,0 in case point missing
            fixed_positions = [
                pos if pos is not None else [0.0, 0.0, 0.0]
                for pos in bones.positions
            ]
            bones_pos.append(fixed_positions)

    bones_pos = np.array(bones_pos).transpose((1, 0, 2))
    colors = [[1, 0, 0] for i in range(len(body_edges))]

    #interpolate zeros when there are missing values
    bones_pos = interpolate_bones_positions(bones_pos)

    return body_edges, bones_pos, colors


def show_animation(file, bones_pos, body_edges, colors, points_indices=None):
    """
        Show the animation of the stickman. Optionally, highlight trajectories of specific giving points points.
        This function were used in first versions, now it's not used anymore but usefull if desired to show the animation.
    """
    # Ensure points_indices is a list if provided
    if points_indices is not None and isinstance(points_indices, int):
        points_indices = [points_indices]

    # Create a point cloud for joints
    keypoints = o3d.geometry.PointCloud()
    keypoints.points = o3d.utility.Vector3dVector(bones_pos[0])

    # Create a LineSet for skeletal connections
    skeleton_joints = o3d.geometry.LineSet()
    skeleton_joints.points = o3d.utility.Vector3dVector(bones_pos[0])
    skeleton_joints.lines = o3d.utility.Vector2iVector(body_edges)
    skeleton_joints.colors = o3d.utility.Vector3dVector(colors)

    # Create LineSets for trajectories if points_indices is provided
    trajectories = {}
    if points_indices is not None:
        for idx in points_indices:
            trajectories[idx] = {
                "points": [],
                "lines": [],
                "geometry": o3d.geometry.LineSet()
            }

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(skeleton_joints)
    vis.add_geometry(keypoints)

    # Add all trajectories to the visualizer if points_indices is provided
    if points_indices is not None:
        for traj in trajectories.values():
            vis.add_geometry(traj["geometry"])

    # Settings for the animation
    frame_rate = file.frame_rate
    num_frames = bones_pos.shape[0]
    interval = 1 / frame_rate

    # vis.get_view_control().set_zoom(0.6)

    for i in range(num_frames):
        # Update skeleton and keypoints positions
        new_joints = bones_pos[i]
        skeleton_joints.points = o3d.utility.Vector3dVector(new_joints)
        keypoints.points = o3d.utility.Vector3dVector(new_joints)

        # Update trajectories for each point if points_indices is provided
        if points_indices is not None:
            for idx in points_indices:
                trajectories[idx]["points"].append(new_joints[idx])
                if len(trajectories[idx]["points"]) > 1:
                    trajectories[idx]["lines"].append([
                        len(trajectories[idx]["points"]) - 2,
                        len(trajectories[idx]["points"]) - 1
                    ])

                trajectory_geometry = trajectories[idx]["geometry"]
                trajectory_geometry.points = o3d.utility.Vector3dVector(np.array(trajectories[idx]["points"], dtype=np.float64))
                if trajectories[idx]["lines"]:
                    trajectory_geometry.lines = o3d.utility.Vector2iVector(np.array(trajectories[idx]["lines"], dtype=np.int32))

        # Update the visualizer
        vis.update_geometry(skeleton_joints)
        vis.update_geometry(keypoints)
        if points_indices is not None:
            for traj in trajectories.values():
                vis.update_geometry(traj["geometry"])

        vis.poll_events()
        vis.update_renderer()
        time.sleep(interval)

    vis.run()


def show_anim(filename):
    """
        Show animation given the filename
    """
    take = csv.Take().readCSV(filename)
    # print("Found rigid bodies:", take.rigid_bodies.keys())
    body_edges, bones_pos, _ = get_bones_position(take)
    colors = [[1, 0, 0] for i in range(len(body_edges))]
    show_animation(take, bones_pos, body_edges, colors)


def show_message(message, message_type="info"):
    """
    Display a standardized message to the user with optional emojis to make the communications more enjoyable.
    """
    emoji_map = {
        "question": "❓",
        "graphs": "📊",
        "stats": "📝",
        "info": "❗",
        "error": "❌",
        "success": "✅",
        "shoulder": "⭐️⭐️⭐️⭐️⭐️\n💪",
        "feet": "⭐️⭐️⭐️⭐️⭐️\n🦵",
        "hips": "⭐️⭐️⭐️⭐️⭐️\n🧍",
        "archery": "🏹",
    }
    emoji = emoji_map.get(message_type, "ℹ️")
    if emoji == "success" or emoji == "question":
        print(f"\n{emoji} {message}")
    else:
        print(f"\n{emoji} {message}")


def ask_yesno(prompt):
    """
        Ask the user a yes/no question
    """
    valid_yes = {'y', 'Y', 'yes', 'YES', 'Yes', ''}
    valid_no = {'n', 'N', 'no', 'NO', 'No'}

    print(f"\n🏅 {prompt} (Y/n)")
    while True:
        option = input("✒️  ").strip()
        if option in valid_yes:
            print("✅ Selected: Yes\n")
            return True
        elif option in valid_no:
            print("✅ Selected: No\n")
            return False
        else:
            print("\n🙅 Invalid, Please respond with 'yes' or 'no' or 'y' or 'n'.")


def save_stats(stats1, stats2, stats3, joint, key=None):
    """
        Save the extracted statistics to a JSON file.
    """
    output_folder = f"output/{joint}/stats/"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{joint}_stats.json")

    if key is not None:
        output_file = os.path.join(output_folder, f"{joint}_{key}_stats.json")

    if stats3 is not None:
        stats = {
            "Correct posture": stats1,
            "Wrong Posture": stats2,
            "Wrong Posture-2": stats3
        }
    else:
        stats = {
            "Correct posture": stats1,
            "Wrong Posture": stats2,
        }

    with open(output_file, "w") as f:
        json.dump(stats, f, indent=4)

    show_message(f"Statistics for the {joint} analysis have been saved in {output_file}.", "stats")
