import os

import optitrack.csv_reader as csv

from utils import get_bones_position, calculate_distances
from utils import show_message, save_stats, analyze_metric_series
from utils import plot_combined_time_and_distribution, plot_metric_over_time, plot_distribution

def analyse_feet(show_plots):
    show_message(f"Analysing feet and toe distance", "feet")

    key = "feet"
    key2 = "toe"
    keyword = "Distance Between Feet"
    keyword_1 = "Distance Between Foot"
    keyword_2 = "Distance Between Toes"
    
    correct = "data/Training_Recording.csv"
    shoulder = "data/Wrong_Foot_Position.csv"

    take_1 = csv.Take().readCSV(correct)
    take_2 = csv.Take().readCSV(shoulder)

    body_edges_1, bones_pos_1, colors_1 = get_bones_position(take_1)
    distances_1 = calculate_distances(bones_pos_1)

    body_edges_2, bones_pos_2, colors_2 = get_bones_position(take_2)
    distances_2 = calculate_distances(bones_pos_2)

    stats1 = analyze_metric_series(distances_1, key)
    stats2 = analyze_metric_series(distances_2, key)

    stats11 = analyze_metric_series(distances_1, key2)
    stats22 = analyze_metric_series(distances_2, key2)
    
    output_folder = f"output/{key}/plots/"
    os.makedirs(output_folder, exist_ok=True)
    
    # combined plot (distribution & time)
    plot_combined_time_and_distribution(
        distances_1, distances_2, None,
        f"{keyword} Over Time (Correct vs Wrong)",
        f'{keyword} Distribution',
        f"Correct {keyword_1}", f"Wrong {keyword_1}", f"Correct {keyword_2}", f"Wrong {keyword_2}",
        f"{keyword}",
        f"{keyword} (cm)",
        key, key2,
        os.path.join(output_folder, "Feet_distance_combined_plot.png"),
        show_plots=show_plots
    )

    # feet distance over time
    plot_metric_over_time(
        distances_1, distances_2, None,
        f"{keyword} Over Time (Correct vs Wrong)",
        f"Correct {keyword}", f"Wrong {keyword}", None,
        f'{keyword}',
        key,
        os.path.join(output_folder, f"Feet_distance_over_time.png"),
        show_plots=False
    )

    # feet distance distribution
    plot_distribution(
        distances_1, distances_2, None,
        f"Distribution of {keyword} (KDE)",
        f"Correct {keyword}", f"Wrong {keyword}", None,
        f"{keyword} (cm)",
        key,
        os.path.join(output_folder, f"Feet_distance_distribution.png"),
        show_plots=False
    )

    # toe distance over time
    plot_metric_over_time(
        distances_1, distances_2, None,
        f"{keyword_2} Over Time (Correct vs Wrong)",
        f"Correct {keyword_2}", f"Wrong {keyword_2}", None,
        f'{keyword_2}',
        key2,
        os.path.join(output_folder, f"Toe_distance_over_time.png"),
        show_plots=False
    )

    # toe distance distribution
    plot_distribution(
        distances_1, distances_2, None,
        f"Distribution of {keyword_2} (KDE)",
        f"Correct {keyword_2}", f"Wrong {keyword_2}", None,
        f"{keyword_2} (cm)",
        key2,
        os.path.join(output_folder, f"Toe_distance_distribution.png"),
        show_plots=False
    )

    show_message(f"Graphs for the feet distance analysis have been saved in {output_folder}", "graphs")
    save_stats(stats1, stats2, None, "feet", None)
    save_stats(stats11, stats22, None, "feet", "toe")
