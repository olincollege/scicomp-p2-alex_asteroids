# Scientific Computing Project 2: Asteroid Family Classification

This repository holds the code for the second project in ENGR3560: Scientific Computing. The benchmark for this project is to identify eight asteroid families to 95% completeness.

My project looks at Heirarchical Clustering Method (HCM) clustering on asteroids. This repository shows the results of two different nearest-neighbor search methods: **KDTree** and **BallTree**, and how they compare to a labeled dataset of asteroid families. KDTree and BallTree are used to efficiently find neighbors within the HCM cutoff radius. The labeled dataset is from the AstDys group, founded by A. Milani: https://newton.spacedys.com/astdys2/index.php?pc=5.

This project is implemented in Python. The datasets used for this project are from the 1919 paper "Groups of Asteroids Probbaly of Common Origin" by Kiyotsugu Hirayama.


## To-do:
- fill out README
- currently data must be downloaded manually, and then the paths need to be changed in the txt_csv_converter.py file -> add 'requests' package here to automate this process
- add pictures of a, e, sin(i) to the key sim variables section
- add checks 


## Key Simulation Variables
`a` - Semi-major axis (AU)

`e` - Eccentricity (unitless)

`sin(i)` - Sin of Orbital Inclination (°)

### Visual Exploration of Asteroid Data
<table>
  <tr>
    <td align="center">
      <img src="images/2D_a_vs_sini.png" width="600"><br>
      Semi-major axis (AU) vs. sin(Inclination) (°)
    </td>
    <td align="center">
      <img src="images/2D_e_vs_sini.png" width="600"><br>
      Eccentricity vs. sin(Inclination) (°)
    </td>
    <td align="center">
      <img src="images/3D_visible_clusters_sini.png" width="500"><br>
      3D representation of clusters (a, e, sin(i))
    </td>
  </tr>
</table>

The 2D and 3D representations show the clusters that appear in the asteroid data when looking at constrainted a, e, and i parameters.

## Datasets Used

### Clustering Dataset

Source: *Numbered and multiopposition asteroids* (AstDys)

This dataset defines the asteroids used as the input data for the clustering algorithms.

Characteristics:
- Includes both numbered asteroids (objecst with well-known orbits) and multi-opposition asteroids (objects witih multiple observations but without assigned numbers).
- Contains **Main Belt** and **Hungaria** asteroids only.

### Labeled Dataset

Source: *Proper elements computed analytically, algorithm version 9 (Numbered asteroids); proper elements* (AstDys)

This dataset is used as the reference validation dataset. It is important to note that this catalog only contains **numbered** asteroids, so **some objects in the clustering dataset do not appear in the labeled dataset.**

Characteristics:

- Contains **numbered** asteroids (no multi-opposition).
- Contains analytically computer proper orbital elements and family designation number.

### Dataset Overlap

The validation characteristics I have chosen to use to assess the correctness of my clustering algorithms only look at asteroids that **appear in both datasets.** This means that multi-opposition asteroids appear in the clustered plots, but are not included in the validation metrics (purity and correctness). Only numbered asteroids with analytical proper elements are used.

## Clustering Algorithms

KDTree and BallTree are spatial indexing clustering algorithm used to speed up nearest-neighbor searches in multi-dimensional data. The two algorithms serve the same purpose, but have different strengths depending on the data. Both algorithms are used under-the-hood for the Heirarchical Clustering Method (HCM), which is often used in asteroid family classification.

### KDTree
https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html

- Works best in low-dimensional data
- Splits data along hyperplanes - split using one dimension at a time

### BallTree
https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html#sklearn.neighbors.BallTree

- Works best in higher-dimensional data
- Splits data into hyperspheres (spheres)

## Usage Examples & Benchmarks

For this project, I specifically chose to look at two nearest-neighbor algorithms: KD trees and ball tree algorithms. Both of these are used to speed up the process of HCM, a distance-based heirarchical clustering algorithm, often used as the standard multiple asteroid family clustering papers. 

I looked at `r` values `0.0012`, `0.0015`, `0.0018`, `0.002`. I did not run any parameter sweeps, but from trial and error these values produce the best results.


The two benchmarks that I used to evaluate my clustering algorithms are `purity` and `completeness`. 

`purity`: correctly clustered asteroids / total clustered asteroids from the merged clustered-labeled dataset

-> *Are all of the asteroids in a cluster determined to be a particular family actually part of that family? How pure are my clusters?*

`completeness`: correctly clustered asteroids / total labeled asteroids from the merged clustered-labeled dataset

-> *How many labeled asteroids did the cluster actually catch? (Unclustered asteroids count as missing)*


### Results Summary Table - average across all families

|    r    | Purity (KDTree) | Completeness (KDTree) | Purity (BallTree) | Completeness (BallTree) |
| ------- | --------------- | --------------------- | ----------------- | ----------------------- |
| 0.0012  |       100%      | 24.40% | 100% | 24.40% |
| 0.0015  |      99.99%     | 34.23%  | 99.99% | 34.23% |
| 0.0018  |      94.64%     | 43.65%  | 94.64% | 43.65% |
| 0.002   |                 |  | 89.07% | 47.05% |


### KD tree Algorithm

The key variable for the kd tree algorithm is r - this is the radius of distance that determines whether or not asteroid neigh

#### r = 0.0018
<table>
  <tr>
    <td align="center">
      <img src="images/a_vs_sini_r0018.png" width="600"><br>
      Semi-major axis (AU) vs. Inclination (°)
    </td>
    <td align="center">
      <img src="images/e_vs_sini_r0018.png" width="600"><br>
      Eccentricity vs. Inclination (°)
    </td>
    <td align="center">
      <img src="images/a_vs_e_vs_sini_r0018.png" width="600"><br>
      3D representation of clusters (a, e, i)
    </td>
  </tr>
</table>

### Ball Tree Algorithm

## Requirements

The `requirements.txt` file contains the required package imports:

- matplotlib~=3.10.8
- numpy~=2.4.2
- pandas~=3.0.0
- scikit_learn~=1.8.0


## How to Use

-> data file is too big to upload to github
--> need to include directions for how to download the data from the website and probably have a script to run to turn it into an excel spreadsheet?

Click on the "Use this template" button in the top right corner to create a new
repository based on this template. If this is for a class project, we ask that
you keep it in the `olincollege` GitHub organization, and that you refrain from
keeping the repository private. This will ensure that relevant people can access
your repository for assessment, etc.

## Code Validation

- reading in the dataset correctly
- visual checks of the data
- check for the function that I'm going to write that checks the clusters from clustering algs to the known clusters from the website

## File Structure

## Author
The creator of this repository is Alex Mineeva (amineeva).

## Sources

Zappalà, V., Cellino, A., Farinella, P., & Knežević, Z. (1990). Asteroid Families. I. Identification by Hierarchical Clustering and Reliability Assessment. The Astronomical Journal, 100, 2030–2046.
https://ui.adsabs.harvard.edu/abs/1990AJ....100.2030Z/abstract

Datasets: https://newton.spacedys.com/astdys2/index.php?pc=5