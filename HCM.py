"""
Contains functions to run Heirarchical Clustering Method (HCM) for asteroids.
"""

##### Imports #####
from kd_tree import kd_tree_clustering
from ball_tree import ball_tree_clustering
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from var_parameters import a_AU_min, a_AU_max, e_min, e_max, sin_I_min, sin_I_max

def run_nearest_neighbor(subset:pd.DataFrame, clustering_alg:str, radius:float)->tuple[np.ndarray, list[list[float]], int]:
    """
    Function to run nearest neighbor algorithm.

    Args:
        subset (pandas DataFrame): Dataframe containing asteroid data limited by a, e, sin(i) value parameters. Must include columns 'a_AU', 'e', 'sin_I'.
        clustering_alg (str): String representing clustering alg to run. Either "kd_tree" or "ball_tree".
        radius (float): Float representing distance cutoff.
    Returns:
        X (numpy ndarray): Numpy array containing asteroids from subset, columns a, e, sin(i).
        clusters (list): list of clusters produced by the selected algorithm, each cluster is a list of indices of the points belonging to that cluster.
        raw_num_clusters (int): Total number of clusters detected before filtering.
    """
    X = subset[['a_AU', 'e', 'sin_I']].values # only running subset!

    if clustering_alg == "kd_tree":
        clusters = kd_tree_clustering(X, radius = radius)
    elif clustering_alg == "ball_tree":
        clusters = ball_tree_clustering(X, radius=radius)
    raw_num_clusters = len(clusters)
    print("Raw number of clusters:", raw_num_clusters)
    return X, clusters, raw_num_clusters



##### Labeling the dataset, removing clusters smaller than 50 #####
def labeling_cleaning_dataset(subset:pd.DataFrame, X:np.ndarray, clusters:list, min_size:int=50)->tuple[np.ndarray, pd.DataFrame]:
    """
    Assign cluster labels to asteroids and filter our small clusters.
    Args:
        subset (pd.DataFrame): DataFrame containing asteroid subset.
        X (pandas DataFrame): Dataframe containing asteroids from subset, columns a, e, sin(i).
        clusters (list): list of clusters produced by the selected algorithm, each cluster is a list of indices of the points belonging to that cluster.
        min_size (int): Int representing minimum number of asteroids in a cluster to consider. Default 50.
    Returns:
        tuple:
            labels (np.ndarray): Array of clusters IDs for each asteroid.
            subset (pandas DataFrame): Updated DataFrame including a 'cluster_id' column.
    """
    labels = np.full(len(X), -1) # -1 if cluster too small

    for cid, cluster in enumerate(clusters):
        if len(cluster) >= min_size:
            labels[cluster] = cid

    subset['cluster_id'] = labels
    return labels, subset



##### saving data for comparison #####
def save_clustering_csvs(df:pd.DataFrame, subset:pd.DataFrame, clusters:list[list[int]], labels:np.ndarray, base_path:str, clustering_alg:str, radius:float, min_size:int=50) -> None:
    """
    Functions saves labeled asteroid dataset and cluster summary csv files.
    Args:
        df (pd.DataFrame): Full asteroid dataset.
        subset (pd.DataFrame): Subset used for clustering.
        clusters (list[list[int]]): Clusters produced by the algorithm.
        labels (np.ndarray): Cluster labels assigned to subset rows.
        base_path (str): Directory where output files will be written.
        clustering_alg (str): Name of clustering algorithm used.
        radius (float): HCM distance cutoff.
        min_size (int, optional): Minimum cluster size used for filtering.
    Returns:
        None
    """
    r_str = str(radius).split(".")[1]

    df['cluster_id'] = -1
    df.loc[subset.index, 'cluster_id'] = labels
    labeled_csv_path = base_path + f"{clustering_alg}_asteroid_clusters_full_r{r_str}.csv"
    df.to_csv(labeled_csv_path, index=False)
    print(f"Labeled dataset saved to: {labeled_csv_path}")

    ##### saving summary dataset #####
    cluster_summary = pd.DataFrame({
        'cluster_id': [cid for cid, c in enumerate(clusters) if len(c) >= min_size],
        'size': [len(c) for c in clusters if len(c) >= min_size],
        }
    )
    summary_csv_path = base_path + f"{clustering_alg}_asteroid_clusters_summary_r{r_str}.csv"
    cluster_summary.to_csv(summary_csv_path, index=False)
    print(f"Summarized dataset saved to: {summary_csv_path}")



##### Visualize the clusters #####
def visualize_cluster_plots(clustering_alg:str, radius:float, labels:np.ndarray, subset:pd.DataFrame, raw_num_clusters:int)->None:
    """
    Generates and saves cluster visualization plots: 
        - a vs. sin(i), e vs. sin(i), a vs. e vs. sin(i)
    Args:
        clustering_alg (str): Name of clustering algorithm used.
        radius (float): HCM distance cutoff.
        labels (np.ndarray): Cluster labels for subset.
        subset (pd.DataFrame): Asteroid subset with cluster labels.
        raw_num_clusters (int): Number of clusters detected before filtering.
    """
    r_str = str(radius).split(".")[1]

    clustered = subset['cluster_id'] >= 0
    unclustered = subset['cluster_id'] == -1
    num_clustered_filtered = len(np.unique(labels[labels >= 0]))

    # --- a vs sin(i) ---
    plt.figure()
    plt.scatter(
        subset.loc[unclustered, 'a_AU'], 
        subset.loc[unclustered, 'sin_I'], 
        c='lightgray', s=0.1, alpha=0.2, label='Unclustered'
    )
    plt.scatter(
        subset.loc[clustered, 'a_AU'], 
        subset.loc[clustered, 'sin_I'], 
        c=subset.loc[clustered, 'cluster_id'], s=0.1, alpha=0.8, cmap='tab20', label='Clusters'
    )
    plt.xlabel("a (AU)")
    plt.ylabel("sin(i)")
    plt.title(f"Semi-major axis (a) vs. Inclination (sin(i)) ({clustering_alg})")
    plt.figtext(0.5, 0.001, f"Raw # of clusters: {raw_num_clusters}, Filtered # of clusters: {num_clustered_filtered}, HCM radius: {radius}", 
                ha="center", fontsize=10)
    plt.savefig(f"{clustering_alg}_a_vs_sini_r{r_str}.png", dpi=300, bbox_inches='tight')
    plt.close()

    # --- e vs sin(i) ---
    plt.figure()
    plt.scatter(
        subset.loc[unclustered, 'e'], 
        subset.loc[unclustered, 'sin_I'], 
        c='lightgray', s=0.1, alpha=0.2, label='Unclustered'
    )
    plt.scatter(
        subset.loc[clustered, 'e'], 
        subset.loc[clustered, 'sin_I'], 
        c=subset.loc[clustered, 'cluster_id'], s=0.1, alpha=0.8, cmap='tab20', label='Clusters'
    )
    plt.xlabel("e")
    plt.ylabel("sin(i)")
    plt.title(f"Eccentricity vs. Inclination (sin(i)) ({clustering_alg})")
    plt.figtext(0.5, 0.001, f"Raw # of clusters: {raw_num_clusters}, Filtered # of clusters: {num_clustered_filtered}, HCM radius: {radius}", 
                ha="center", fontsize=10)
    plt.savefig(f"{clustering_alg}_e_vs_sini_r{r_str}.png", dpi=300, bbox_inches='tight')
    plt.close()

    # --- 3D plot ---
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot unclustered points in gray
    # ax.scatter(
    #     subset.loc[unclustered, 'a_AU'],
    #     subset.loc[unclustered, 'e'],
    #     subset.loc[unclustered, 'sin_I'],
    #     c='lightgray', s=0.01, alpha=0.2, label='Unclustered'
    # )

    sc = ax.scatter(
        subset.loc[clustered, 'a_AU'],
        subset.loc[clustered, 'e'],
        subset.loc[clustered, 'sin_I'],
        c=subset.loc[clustered, 'cluster_id'],
        s=0.01,
        alpha=0.8,
        cmap='tab20',
        label='Clusters'
    )

    ax.set_xlabel('Semi-major axis (a) [AU]')
    ax.set_ylabel('Eccentricity (e)')
    ax.set_zlabel('Inclination (sin(i)))')

    ax.set_xlim(a_AU_min, a_AU_max)
    ax.set_ylim(e_min, e_max)
    ax.set_zlim(sin_I_min, sin_I_max)

    ax.set_title(f"Proper Element Space (a, e, i) | HCM radius: {radius} | {clustering_alg}")
    plt.savefig(f"{clustering_alg}_a_vs_e_vs_sini_r{r_str}.png", dpi=300, bbox_inches='tight')

    plt.show()