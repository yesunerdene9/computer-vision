import os

import optitrack.csv_reader as csv

from utils import show_message, save_stats
from utils import get_bones_position, calculate_angles, analyze_metric_series
from utils import plot_metric_over_time, plot_distribution, plot_combined_time_and_distribution


def analyse_shoulder(show_plots):
    show_message(f"Analysing shoulder posture", "shoulder")

    key = "shoulder"
    keyword = "Shoulder Raise Angle"
    
    correct = "dataset/Training_Recording.csv"
    shoulder = "dataset/Wrong_Shoulder_Position.csv"

    take_1 = csv.Take().readCSV(correct)
    take_2 = csv.Take().readCSV(shoulder)

    body_edges_1, bones_pos_1, colors_1 = get_bones_position(take_1)
    angles_1 = calculate_angles(bones_pos_1)

    body_edges_2, bones_pos_2, colors_2 = get_bones_position(take_2)
    angles_2 = calculate_angles(bones_pos_2)

    stats1 = analyze_metric_series(angles_1, key)
    stats2 = analyze_metric_series(angles_2, key)

    output_folder = f"output/{key}/plots/"
    os.makedirs(output_folder, exist_ok=True)

    # combined plot (distribution & time)
    plot_combined_time_and_distribution(
        angles_1, angles_2, None,
        f"{keyword} Over Time (Correct vs Wrong)",
        f"{keyword} Distribution",
        f"Correct {keyword} (Straight)", f"Wrong {keyword}", None, None,
        f"{keyword}",
        "Angle (Degree)",
        key, None,
        os.path.join(output_folder, "Shoulder_raise_angle_combined_plot.png"),
        show_plots=show_plots
    )

    # shoulder raise over time
    plot_metric_over_time(
        angles_1, angles_2, None,
        f"{keyword} Over Time (Correct vs Wrong)",
        "Correct {keyword} (Straight)", f"Wrong {keyword}", None,
        f"{keyword}",
        key,
        os.path.join(output_folder, f"Shoulder_raise_angle_over_time.png"),
        show_plots=False
    )

    # shoulder raise distribution
    plot_distribution(
        angles_1, angles_2, None,
        f"{keyword} Distribution",
        f"Correct {keyword} (Straight)", f"Wrong {keyword}", None,
        "Angle (Degree)",
        key,
        os.path.join(output_folder, f"Shoulder_raise_angle_distribution.png"),
        show_plots=False
    )

    show_message(f"Graphs for the shoulder analysis have been saved in {output_folder}", "graphs")
    save_stats(stats1, stats2, None, key, None)
