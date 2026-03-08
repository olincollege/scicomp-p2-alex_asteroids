"""
Asteroid family detection through HCM.
"""

# Imports #
import numpy as np
from sklearn.neighbors import KDTree
import pandas as pd

# set these values!! #
radius = 0.002
a_AU_min = 2.5 #2
a_AU_max = 3.3 #3.5
# a_AU_min = 2.825
# a_AU_max = 2.958
e_min = 0
e_max = 0.5
sin_I_min = 0
sin_I_max = np.sin(np.radians(20))



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


# HCM clustering function #
def hcm_clustering(data, radius):
    """
    data: Nx3 array of (a, e, sin(i))
    radius: distance cutoff
    """

    # building KDTree - spatial index to avoid checking every asteroid against every other asteroid
    tree = KDTree(data)

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

            # find neighbors within radius of initial asteroid 'i'
            neighbors = tree.query_radius(data[idx].reshape(1, -1), r=radius)[0]

            # finding neighbors of the neighbors, add to stack to be visited by alg to potentially add to cluster
            for nb in neighbors:
                if not visited[nb]:
                    stack.append(nb)
        # all neighbors looked at, cluster is done
        clusters.append(cluster)
    
    # return list of all clusters
    return clusters



# Running the algorithm
X = subset[['a_AU', 'e', 'sin_I']].values # only running subset!

clusters = hcm_clustering(X, radius=radius)

print("Number of clusters:", len(clusters))

# Labeling the dataset
labels = np.full(len(X), -1)

for cid, cluster in enumerate(clusters):
    for idx in cluster:
        labels[idx] = cid

subset['cluster'] = labels


# Visualize the clusters
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # ensures 3D projection works

# --- a vs sin(i) ---
plt.figure()
plt.scatter(subset['a_AU'], subset['sin_I'], c=subset['cluster'], s=2)
plt.xlabel("a (AU)")
plt.ylabel("sin(i)")
plt.title("Semi-major axis (a) vs. Inclination (sin(i))")
# plt.show()
plt.savefig("a_vs_sini.png")
plt.close()

# --- e vs sin(i) ---
plt.figure()
plt.scatter(subset['e'], subset['sin_I'], c=subset['cluster'], s=2)
plt.xlabel("e")
plt.ylabel("sin(i)")
plt.title("Eccentricity vs. Inclination (sin(i))")
# plt.show()
plt.savefig("e_vs_sini.png")
plt.close()

# --- 3D plot ---
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(
    subset['a_AU'],
    subset['e'],
    subset['sin_I'],
    c=subset['cluster'],   # color by cluster
    s=1,
    alpha=0.2
)

ax.set_xlabel('Semi-major axis (a) [AU]')
ax.set_ylabel('Eccentricity (e)')
ax.set_zlabel('Inclination (i)')

ax.set_xlim(2, 3.5)
ax.set_ylim(0, 0.3)
ax.set_zlim(0, 20)

ax.set_title('Proper Element Space (a, e, i)')

plt.show()