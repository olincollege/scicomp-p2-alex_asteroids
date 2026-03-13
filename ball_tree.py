"""
Asteroid family detection through ball tree clustering.
"""

##### Imports #####
import numpy as np
from sklearn.neighbors import BallTree
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# user inputs #
from user_inputs import a_AU_min, a_AU_max, e_min, e_max, sin_I_min, sin_I_max

# set this value!! #
radius = 0.0015
clustering_alg = "ball_tree"




# Loading in dataset #
base_path = "/mnt/c/Users/amineeva/OneDrive - Olin College of Engineering/2025-2026/Semester 2/Scientific Computing/Project 2 - Asteroids/"
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

r_str = str(radius).split(".")[1]


# kd_tree clustering function #
def ball_tree_clustering(data:np.array, radius:float)->list:
    """
    Run HCM clustering using ball_tree clustering algorithm. Returns found clusters.

    Args:
        data (Numpy Array): Nx3 array of (a, e, sin(i)).
        radius (float): Float representing distance cutoff.

    Returns:
        clusters (list): list of clusters, each cluster is a list of indices.
    """

    # building BallTree - spatial index to avoid checking every asteroid against every other asteroid
    tree = BallTree(data)

    n = len(data)

    visited = np.zeros(n, dtype=bool) # flags whether asteroid has been visited by algorithm
    clusters = [] # list to hold discovered clusters

    # looping through all asteroids - tracks clusters
    for i in range(n):

        if visited[i]: # skip algorithm if asteroid already visited
            continue

        # start new cluster
        cluster = []
        stack = [i] # asteroids that still need to be checked in the cluster

        while stack:
            idx = stack.pop() # next asteroid to be checked

            if visited[idx]: # skip algorithm if asteroid already visited
                continue

            # if asteroid not already visited (as i), flag as visited and add to appendix
            visited[idx] = True
            cluster.append(idx)

            # find neighbors within radius of intial asteroi 'i', needs 2D query
            neighbors = tree.query_radius(data[idx].reshape(1, -1), r=radius)[0]

            # finding neighbors of the neighbors, add to stack to be visited by alg to potentially add to cluster
            for nb in neighbors:
                if not visited[nb]:
                    stack.append(nb)
        # all neighbors looked at, cluster is done
        clusters.append(cluster)
    
    # return list of all clusters
    return clusters






######################################### THIS PART IS FULLY COPIED FROM KD_TREE ###########################################
# Running the algorithm

def run_nearest_neighbor(subset:pd.DataFrame, clustering_alg:str, radius:float)->tuple[pd.DataFrame, list]:
    """
    Function to run nearest neighbor algorithm.

    Args:
        subset (pandas DataFrame): Dataframe containing asteroid data limited by a, e, sin(i) value parameters. Must include columns 'a_AU', 'e', 'sin_I'.
        clustering_alg (str): String representing clustering alg to run. Either "kd_tree" or "ball_tree".
        radius (float): Float representing distance cutoff.
    Returns:
        X (pandas DataFrame): Dataframe containing asteroids from subset, columns a, e, sin(i).
        clusters (list): list of clusters produced by the selected algorithm, each cluster is a list of indices of the points belonging to that cluster.
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
def labeling_cleaning_dataset(X:pd.DataFrame, clusters:list, min_size:int=50)->pd.DataFrame:
    """
    Args:
        X (pandas DataFrame): Dataframe containing asteroids from subset, columns a, e, sin(i).
        clusters (list): list of clusters produced by the selected algorithm, each cluster is a list of indices of the points belonging to that cluster.
        min_size (int): Int representing minimum number of asteroids in a cluster to consider. Default 50.
    Returns:
        subset (pandas DataFrame): DataFrame containing subset of asteroid data with labeled column.
    """
    labels = np.full(len(X), -1) # -1 if cluster too small

    for cid, cluster in enumerate(clusters):
        if len(cluster) >= min_size:
            labels[cluster] = cid

    subset['cluster_id'] = labels
    return labels, subset



##### saving data for comparison #####
def save_clustering_csvs(clusters:list, labels, min_size:int=50):
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
def visualize_cluster_plots(clustering_alg, radius, labels, subset, raw_num_clusters:int):
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
    plt.title("Semi-major axis (a) vs. Inclination (sin(i)) (Ball Tree)")
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
    plt.title("Eccentricity vs. Inclination (sin(i)) (Ball Tree)")
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