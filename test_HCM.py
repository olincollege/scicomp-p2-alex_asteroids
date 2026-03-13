"""Unit tests for HCM.py"""

from HCM import run_nearest_neighbor
import pytest
import pandas as pd
import numpy as np


##### run_nearest_neighbor #####
def make_test_dataframe():
    """
    Small synthetic asteroid dataset for testing.
    Two obvious clusters.
    """
    data = {
        "a_AU":  [2.1, 2.11, 2.12, 3.0, 3.01, 3.02],
        "e":     [0.1, 0.11, 0.1,  0.2, 0.21, 0.2],
        "sin_I": [0.05,0.051,0.052,0.1, 0.101,0.102]
    }
    return pd.DataFrame(data)


def test_run_nearest_neighbor_output_types():
    df = make_test_dataframe()

    X, clusters, raw_num_clusters = run_nearest_neighbor(
        subset=df,
        clustering_alg="kd_tree",
        radius=0.02
    )

    assert isinstance(X, np.ndarray)
    assert isinstance(clusters, list)
    assert isinstance(raw_num_clusters, int)


def test_run_nearest_neighbor_shape():
    df = make_test_dataframe()

    X, clusters, _ = run_nearest_neighbor(
        subset=df,
        clustering_alg="kd_tree",
        radius=0.02
    )

    assert X.shape == (6, 3)


def test_clusters_not_empty():
    df = make_test_dataframe()

    _, clusters, raw_num_clusters = run_nearest_neighbor(
        subset=df,
        clustering_alg="kd_tree",
        radius=0.02
    )

    assert raw_num_clusters > 0
    assert all(isinstance(c, list) for c in clusters)


def test_kdtree_balltree_same_results():
    df = make_test_dataframe()

    _, clusters_kd, _ = run_nearest_neighbor(
        subset=df,
        clustering_alg="kd_tree",
        radius=0.02
    )

    _, clusters_ball, _ = run_nearest_neighbor(
        subset=df,
        clustering_alg="ball_tree",
        radius=0.02
    )

    # compare cluster sizes (order can differ)
    kd_sizes = sorted([len(c) for c in clusters_kd])
    ball_sizes = sorted([len(c) for c in clusters_ball])

    assert kd_sizes == ball_sizes