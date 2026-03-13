# Scientific Computing Project 2: Asteroid Family Classification

This repository holds the code for the second project in ENGR3560: Scientific Computing. The benchmark for this project is to identify eight asteroid families to 95% completeness.

My project looks at Heirarchical Clustering Method (HCM) clustering on asteroids. This repository shows the results of two different nearest-neighbor search methods: **KDTree** and **BallTree**, and how they compare to a labeled dataset of asteroid families. KDTree and BallTree are used to efficiently find neighbors within the HCM cutoff radius. The labeled dataset is from the AstDys group, founded by A. Milani: https://newton.spacedys.com/astdys2/index.php?pc=5.

This project is implemented in Python. The datasets used for this project are from the 1919 paper "Groups of Asteroids Probbaly of Common Origin" by Kiyotsugu Hirayama.


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

The validation characteristics I have chosen to use to assess the correctness of my clustering algorithms only look at asteroids that **appear in both datasets.** This means that multi-opposition asteroids appear in the clustered plots, but are not included in the validation metrics (purity and complteness). Only numbered asteroids with analytical proper elements are used.

## Nearest-Neighbor Algorithms

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


The two benchmarks that I used to evaluate my clustering algorithms are ***purity*** and ***completeness***. 

***purity***: correctly clustered asteroids / total clustered asteroids from the merged clustered-labeled dataset

-> *Are all of the asteroids in a cluster determined to be a particular family actually part of that family? How pure are my clusters?*

***completeness***: correctly clustered asteroids / total labeled asteroids from the merged clustered-labeled dataset

-> *How many labeled asteroids did the cluster actually catch? (Unclustered asteroids count as missing)*


### Results Summary Table - average across all families

|    r    | Purity (KDTree) | Completeness (KDTree) | Purity (BallTree) | Completeness (BallTree) |
| ------- | --------------- | --------------------- | ----------------- | ----------------------- |
| 0.0012  |       100%      | 24.40% | 100% | 24.40% |
| 0.0015  |      99.99%     | 34.23%  | 99.99% | 34.23% |
| 0.0018  |      94.64%     | 43.65%  | 94.64% | 43.65% |
| 0.002   |      89.07%     | 47.05% | 89.07% | 47.05% |


You will notice that the results summary table, which averages results across all non-exluded clusters (excluded if there are fewer than a minimum number of asteroids (50)) are identical across the two different nearest-neighbor search methods. 

KDTree and BallTree produced identical clustering results because both perform the exact same Euclidian radius queries; they differ only in internal search efficiency, not in the neighbors returned. The table below shows the runtime difference (minutes) across different `r` values.

| r | KDTree | BallTree |
|---| --- | ---- |
|0.001 |4:13 | 9:19 |
|0.0015 | 4:21 | 9:21 |
|0.002 | 4:50 | 9:36 |




### KD tree Algorithm

#### r = 0.0018
<table>
  <tr>
    <td align="center">
      <img src="images/kd_tree/a_vs_sini_r0018.png" width="600"><br>
      Semi-major axis (AU) vs. sin(Inclination) (°)
    </td>
    <td align="center">
      <img src="images/kd_tree/e_vs_sini_r0018.png" width="600"><br>
      Eccentricity vs. sin(Inclination) (°)
    </td>
    <td align="center">
      <img src="images/kd_tree/a_vs_e_vs_sini_r0018.png" width="600"><br>
      3D representation of clusters (a, e, sin(i))
    </td>
  </tr>
</table>
<table>
  <tr>
    <td align="center">
      <img src="images/kd_tree/kdtree_r0018_completeness.png" width="600"><br>
      Completeness Plot
    </td>
    <td align="center">
      <img src="images/kd_tree/kdtree_r0018_purity.png" width="600"><br>
      Purity Plot
    </td>
  </tr>
</table>

### Ball Tree Algorithm
#### r = 0.0018
<table>
  <tr>
    <td align="center">
      <img src="images/ball_tree/ball_tree_a_vs_sini_r0018.png" width="600"><br>
      Semi-major axis (AU) vs. sin(Inclination) (°)
    </td>
    <td align="center">
      <img src="images/ball_tree/ball_tree_e_vs_sini_r0018.png" width="600"><br>
      Eccentricity vs. sin(Inclination) (°)
    </td>
    <td align="center">
      <img src="images/ball_tree/ball_tree_a_vs_e_vs_sini_r0018.png" width="600"><br>
      3D representation of clusters (a, e, sin(i))
    </td>
  </tr>
</table>
<table>
  <tr>
    <td align="center">
      <img src="images/ball_tree/balltree_r0018_completeness.png" width="600"><br>
      Completeness Plot
    </td>
    <td align="center">
      <img src="images/ball_tree/balltree_r0018_purity.png" width="600"><br>
      Purity Plot
    </td>
  </tr>
</table>

### HCM Benchmark Results (r = 0.0018)

Here are my top 8 asteroid families evaluated using the HCM clustering pipeline.

| Family ID | Total Family Asteroids | Correctly Clustered | Completeness | Purity | Cluster Size | Correctness (Full) |
|----------|-----------------------|--------------------|-------------|-------|-------------|-------------------|
| 606 | 1012 | 1012 | 1.000 | 1.000 | 1160 | 0.872 |
| 396 | 1466 | 1466 | 1.000 | 1.000 | 1635 | 0.897 |
| 3815 | 1782 | 1782 | 1.000 | 1.000 | 1975 | 0.902 |
| 1189 | 184 | 184 | 1.000 | 1.000 | 208 | 0.885 |
| 1547 | 1641 | 1641 | 1.000 | 1.000 | 1785 | 0.919 |
| 3 | 3798 | 3784 | 0.996 | 1.000 | 4336 | 0.873 |
| 618 | 477 | 475 | 0.996 | 0.981 | 564 | 0.842 |
| 293 | 1706 | 1696 | 0.994 | 1.000 | 2030 | 0.835 |

This table displays the families with the highest completeness (`Completeness`) values, as taken from my HCM clustering algorithm. Using this metric, all 8 of my families fulfill the 95% correctness criteria. However, there are important considerations to take into account when using this algorithm. A big consideration is that I use the merged dataset to compute the `Completeness` and `Purity` values, meaning that I'm only using asteroids that appear in **both** datasets (clustering and labeled). Doing so excludes multi-opposition asteroids and main belt asteroids that are locked in secular resonance, which means that the results aren't that useful for capturing the "true" completeness of each asteroid family. I have included the column `Correctness (Full)`, which compares the number of correctly clustered asteroids to the number of asteroids per family in the labeled dataset, giving a slightly more realistic value. 

## Requirements

The `requirements.txt` file contains the required package imports:

- matplotlib~=3.10.8
- numpy~=2.4.2
- pandas~=3.0.0
- scikit_learn~=1.8.0


## How to Use

### Pt 1: Clone the repository
```
git clone git@github.com:olincollege/scicomp-p2-alex_asteroids.git
cd scicomp-p2-alex_asteroids/
```

Install dependencies:
```
pip install -r requirements.txt
```

### Pt 2: Download data files
The data files from AstDys are too large to upload to GitHub, so you will need to download them directly off of AstDys (https://newton.spacedys.com/astdys2/index.php?pc=5). 

#### Step 1: Navigate the AstDys and locate datasets
<img src="images/Datasets_to_download.png" width="600">

`1` - clustering dataset

`2` - labeled dataset

#### Step 2: Click on each dataset, `ctrl s`, save to common folder
I recommend creating a folder where everything for these runs can be stored and outputed.

`1` - save this file as `Synthetic_Proper_Elements_Hirayama_full_dataset.txt`

`2` - save this file as `all_tro.members.txt`

#### Step 3: Run both files through `txt_csv_converter.py`
Update the `base_path` and the and the input/output file endings: `asteroid_data_download_path`, `asteroid_data_output_path`.

`1` - this file should be saved as `Synthetic_Proper_Elements_Hirayama_full_dataset.csv`

`2` - this file should be saved as `all_tro.members.csv`

### Pt 3: Run HCM

#### Step 1: Update user inputs
In `main.py` update the `user inputs` section. You must change the `base_path` to match where you have stored the clustering and labeling datasets. The default run values are:

```
radius = 0.002
clustering_alg = "kd_tree" # ball_tree
min_size = 50
```

#### Step 2: Run the simulation
```
python main.py
```


## Code Validation

Due to a smaller amount of time on this project, I was unable to add the code validation and fortification procedures to my desired amount. However, throughout my process I output lots of plots, which should be used to visually check the clustering algorithm. Another good check to do is to make sure that the data you're using is the correct data - the datasets I used are detailed elsehwere in this README, and it is good to confirm that you use the same ones. 

- reading in the dataset correctly
- visual checks of the data
- check for the function that I'm going to write that checks the clusters from clustering algs to the known clusters from the website

## File Structure

`Asteroid_family_exploration.ipynb` - Initial Jupyter Notebook, plots general asteroid data.

`HCM.py` - Contains functions to run Heirarchical Clustering Method (HCM) for asteroids.

`ball_tree.py` - Ball Tree nearest neighbor algorithm.

`benchmark_validation.py` - Compares clustered data to labeled data, gives a correctness score. The benchmark for this project is 95% correctness, calculates purity and completeness scores.

`kd_tree.py` - KDTree nearest neighbor algorithm.

`main.py` - Contains main script to run machine learning algorithms on the data.

`txt_csv_converter.py` - Converts .txt dataset into usable .csv file that will run with the clustering algorithms.

`var_parameters.py` - Contains user inputs parameters for all files in asteroid clustering.

## Author
The creator of this repository is Alex Mineeva (amineeva).

## Sources

Zappalà, V., Cellino, A., Farinella, P., & Knežević, Z. (1990). Asteroid Families. I. Identification by Hierarchical Clustering and Reliability Assessment. The Astronomical Journal, 100, 2030–2046.
https://ui.adsabs.harvard.edu/abs/1990AJ....100.2030Z/abstract

Datasets: https://newton.spacedys.com/astdys2/index.php?pc=5