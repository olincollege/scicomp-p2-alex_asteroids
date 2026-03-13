"""
Asteroid family detection through kd_tree clustering.
"""

##### Imports #####
import numpy as np
from sklearn.neighbors import KDTree

# kd_tree clustering function #
def kd_tree_clustering(data:np.ndarray, radius:float)->list:
    """
    Run HCM clustering using kd_tree clustering algorithm. Returns found clusters.

    Args:
        data (Numpy Array): Nx3 array of (a, e, sin(i))
        radius (float): distance cutoff

    Returns:
        clusters (list): List containing all clusters found with kd_tree algorithm.
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