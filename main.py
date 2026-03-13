"""
Contains main script to run machine learning algorithms on the data.
"""

##### Imports #####
import pandas as pd
from var_parameters import a_AU_min, a_AU_max, e_min, e_max, sin_I_min, sin_I_max
from ball_tree import ball_tree_clustering
from kd_tree import kd_tree_clustering
import HCM
from benchmark_validation import run_benchmarking


##### User Inputs #####
base_path = "/mnt/c/Users/amineeva/OneDrive - Olin College of Engineering/2025-2026/Semester 2/Scientific Computing/Project 2 - Asteroids/"
radius = 0.002
clustering_alg = "kd_tree" # ball_tree
min_size = 50


# Loading in dataset #
asteroid_data_output_path = base_path + "Synthetic_Proper_Elements_Hirayama_full_dataset.csv"
df = pd.read_csv(asteroid_data_output_path)

# getting subset of data
subset = df[
    (df['a_AU'] > a_AU_min) &
    (df['a_AU'] < a_AU_max) &
    (df['sin_I'] >= sin_I_min) &
    (df['sin_I'] <= sin_I_max) &
    (df['e'] > e_min) &
    (df['e'] < e_max)
].copy()


# Run Clustering
X, clusters, raw_num_clusters = HCM.run_nearest_neighbor(subset, clustering_alg, radius)
labels, subset = HCM.labeling_cleaning_dataset(subset, X, clusters, min_size)
HCM.save_clustering_csvs(df, subset, clusters, labels, base_path, clustering_alg, radius, min_size)
HCM.visualize_cluster_plots(clustering_alg, radius, labels, subset, raw_num_clusters)

# Run Benchmarking
run_benchmarking(clustering_alg, radius, base_path)


