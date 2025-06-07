import os

import optitrack.csv_reader as csv

from utils import user_message, save_stats, analyze_metric_series
from utils import get_bones_position, calculate_angles, calculate_hip_drop
from utils import plot_metric_over_time, plot_distribution, plot_combined_time_and_distribution

def analyse_hips(show_plots):
    user_message(f"Analysing hips posture", "hips")

    key = "hips"
    
    key_4 = "leg_tilt"
    key_3 = "hips_drop"
    key_1 = "hips_raise"
    key_2 = "spine_tilt"

    keyword_3 = "Hips Drop"
    keyword_1 = "Hip Raise Angle"
    keyword_2 = "Spine Tilt Angle"
    keyword_4 = "Back Leg Tilt Angle"
    
    correct = "data/Training_Recording.csv"
    hips_1 = "data/Wrong_Hips_Position.csv"
    hips_2 = "data/Wrong_Hips_Position_3.csv"

    take_1 = csv.Take().readCSV(correct)
    take_2 = csv.Take().readCSV(hips_1)
    take_3 = csv.Take().readCSV(hips_2)

    body_edges_1, bones_pos_1, colors_1 = get_bones_position(take_1)
    angles_1 = calculate_angles(bones_pos_1)

    body_edges_2, bones_pos_2, colors_2 = get_bones_position(take_2)
    angles_2 = calculate_angles(bones_pos_2)

    body_edges_3, bones_pos_3, colors_3 = get_bones_position(take_3)
    angles_3 = calculate_angles(bones_pos_3)

    drop_1 = calculate_hip_drop(bones_pos_1)
    drop_2 = calculate_hip_drop(bones_pos_2)
    drop_3 = calculate_hip_drop(bones_pos_3)

    stats11  = analyze_metric_series(angles_1, key_1)
    stats22 = analyze_metric_series(angles_2, key_1)
    stats33 = analyze_metric_series(angles_3, key_1)

    stats111 = analyze_metric_series(angles_1, key_2)
    stats222 = analyze_metric_series(angles_2, key_2)
    stats333 = analyze_metric_series(angles_3, key_2)

    stats1111 = analyze_metric_series(drop_1, key_3)
    stats2222 = analyze_metric_series(drop_2, key_3)
    stats3333 = analyze_metric_series(drop_3, key_3)

    stats11111 = analyze_metric_series(angles_1, key_4)
    stats22222 = analyze_metric_series(angles_2, key_4)
    stats33333 = analyze_metric_series(angles_3, key_4)

    # --- Hips Drop ---

    output_folder = f"output/{key}/plots/{key_3}"
    os.makedirs(output_folder, exist_ok=True)

    # combined plot (distribution & time)
    plot_combined_time_and_distribution(
        drop_1, drop_2, drop_3,
        f"{keyword_3} Over Time",
        f"{keyword_3} Distribution",
        f"Correct {keyword_3}", f"Wrong {keyword_3} (to the Left)", f"Wrong {keyword_3} (to the Right)", None,
        f"{keyword_3}",
        "Angle (Degree)",
        key_3, None,
        os.path.join(output_folder, "Hips_drop_combined_plot.png"),
        show_plots=show_plots
    )

    # hips drop over time
    plot_metric_over_time(
        drop_1, drop_2, drop_3,
        f"{keyword_3}s Over Time",
        f"Correct {keyword_3}", f"Wrong {keyword_3} (to the Left)", f"Wrong {keyword_3} (to the Right)",
        f"{keyword_3}",
        key_3,
        os.path.join(output_folder, f"Hips_drop_over_time.png"),
        show_plots=False
    )

    # hips drop distribution
    plot_distribution(
        drop_1, drop_2, drop_3,
        f"Distribution of {keyword_3} (KDE)",
        f"Correct {keyword_3}", f"Wrong {keyword_3} (to the Left)", f"Wrong {keyword_3} (to the Right)",
        f"Angle (Degree)",
        key_3,
        os.path.join(output_folder, f"Hips_drop_distribution.png"),
        show_plots=False
    )

    user_message(f"Graphs for the hips drop analysis have been saved in {output_folder}", "graphs")


    # --- Back Leg Tilt Angle --- #

    output_folder = f"output/{key}/plots/{key_4}"
    os.makedirs(output_folder, exist_ok=True)

    # combined plot (distribution & time)
    plot_combined_time_and_distribution(
        angles_1, angles_2, angles_3,
        f"{keyword_4} Over Time (relative to vertical plane)",
        f"{keyword_4} Distribution",
        f"Correct {keyword_4}", f"Wrong {keyword_4} (to the Left)", f"Wrong {keyword_4} (to the Right)", None,
        f"{keyword_4}", 
        f"Angle (Degree)",
        key_4, None,
        os.path.join(output_folder, "Back_leg_tilt_combined_plot.png"),
        show_plots=show_plots
    )

    # back leg tilt angle over time
    plot_metric_over_time(
        angles_1, angles_2, angles_3,
        f"{keyword_4} Over Time (relative to vertical plane)",
        f"Correct {keyword_4}", f"Wrong {keyword_4} (to the Left)", f"Wrong {keyword_4} (to the Right)",
        f'{keyword_4}',
        key_4,
        os.path.join(output_folder, f"Back_leg_tilt_over_time.png"),
        show_plots=False
    )

    # back leg tilt angle distribution
    plot_distribution(
        angles_1, angles_2, angles_3,
        f"{keyword_4} Distribution",
        f"Correct {keyword_4}", f"Wrong {keyword_4} (to the Left)", f"Wrong {keyword_4} (to the Right)",
        f"Angle (Degree)",
        key_4,
        os.path.join(output_folder, f"Back_leg_tilt_distribution.png"),
        show_plots=False
    )

    user_message(f"Graphs for the leg tilt analysis have been saved in {output_folder}", "graphs")


    # --- Spine Tilt Angle - Vertical plane  --- #

    output_folder = f"output/{key}/plots/{key_2}"
    os.makedirs(output_folder, exist_ok=True)

    # combined plot (distribution & time)
    plot_combined_time_and_distribution(
        angles_1, angles_2, angles_3,
        f"{keyword_2} Over Time (relative to vertical plane)",
        f"{keyword_2} Distribution",
        f"Correct {keyword_2}", f"Wrong {keyword_2} (to the Left)", f"Wrong {keyword_2} (to the Right)", None,
        f"{keyword_2}", 
        f"Angle (Degree)",
        key_2, None,
        os.path.join(output_folder, "Spine_tilt_combined_plot.png"),
        show_plots=show_plots
    )

    # spine tilt angle over time
    plot_metric_over_time(
        angles_1, angles_2, angles_3,
        f"{keyword_2} Over Time (relative to vertical plane)",
        f"Correct {keyword_2}", f"Wrong {keyword_2} (to the Left)",  f"Wrong {keyword_2} (to the Right)",
        f"{keyword_2}", 
        key_2,
        os.path.join(output_folder, f"Spine_tilt_over_time.png"),
        show_plots=False,
    )

    # spine tilt angle distribution
    plot_distribution(
        angles_1, angles_2, angles_3,
        f'{keyword_2} Distribution',
        f"Correct {keyword_2}", f"Wrong {keyword_2} (to the Left)", f"Wrong {keyword_2} (to the Right)",
        "Angle (Degree)",
        key_2,
        os.path.join(output_folder, f"Spine_tilt_distribution.png"),
        show_plots=False,
    )

    user_message(f"Graphs for the spine tilt analysis have been saved in {output_folder}", "graphs")


    # --- Hip Raise Angle - Horizontal plane  --- #

    output_folder = f"output/{key}/plots/{key_1}"
    os.makedirs(output_folder, exist_ok=True)


    # combined plot (distribution & time)
    plot_combined_time_and_distribution(
        angles_1, angles_2, angles_3,
        f"{keyword_1} Over Time (relative to horizontal plane)",
        f"{keyword_1} Distribution",
        f"Correct {keyword_1}", f"Wrong {keyword_1} (to the Left)", f"Wrong {keyword_1} (to the Right)", None,
        f"{keyword_1}", 
        "Angle (Degree)",
        key_1, None,
        os.path.join(output_folder, "Hips_raise_combined_plot.png"),
        show_plots=show_plots
    )

    # hips raise angle over time
    plot_metric_over_time(
        angles_1, angles_2, angles_3,
        f"{keyword_1} Over Time (relative to horizontal plane)",
        f"Correct {keyword_1}", f"Wrong {keyword_1} (to the Left)", f"Wrong {keyword_1} (to the Right)",
        f"{keyword_1}",
        key_1,
        os.path.join(output_folder, f"Hips_raise_over_time.png"),
        show_plots=False
    )

    # hips raise angle distribution
    plot_distribution(
        angles_1, angles_2, angles_3,
        f"{keyword_1} Distribution",
        f"Correct {keyword_1}", f"Wrong {keyword_1} (to the Left)", f"Wrong {keyword_1} (to the Right)",
        f"Angle (Degree)",
        key_1,
        os.path.join(output_folder, f"Hips_raise_distribution.png"),
        show_plots=False
    )


    user_message(f"Graphs for the hips raise analysis have been saved in {output_folder}", "graphs")

    save_stats(stats11, stats22, stats33, "hips", key_1)
    save_stats(stats111, stats222, stats333, "hips", key_2)
    save_stats(stats1111, stats2222, stats3333, "hips", key_3)
    save_stats(stats11111, stats22222, stats33333, "hips", key_4)
