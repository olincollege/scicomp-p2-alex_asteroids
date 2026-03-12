"""
Compares clustered data to labeled data, gives a correctness score.
The benchmark for this project is 95% correctness.
Metrics:
    Purity: correctly clustered asteroids / total clustered asteroids from labaled dataset
        -> are all of the asteroids in the cluster determined to be a particular family actually part of that family?
        -> How pure are my clusters? (ignoring unclustered (-1) asteroids)
    Accuracy: correctly clustered asteroids / all labeled asteroids
        -> how many of the labeled asteroids made it into the cluster?
        -> How many labeled asteroids did the cluster actually get? (unclustered asteroids count as missing)

"""

##### Imports #####
import pandas as pd
import matplotlib.pyplot as plt


##### Load in datasets #####
# labeled dataset
base_path = "/mnt/c/Users/amineeva/OneDrive - Olin College of Engineering/2025-2026/Semester 2/Scientific Computing/Project 2 - Asteroids/"
validation_data_path = base_path + "all_tro.members.csv"
df_labeled = pd.read_csv(validation_data_path)

# cluster dataset
base_path = "/mnt/c/Users/amineeva/OneDrive - Olin College of Engineering/2025-2026/Semester 2/Scientific Computing/Project 2 - Asteroids/"
clustered_data_path = base_path + "asteroid_clusters_full_r0012.csv"
df_clustered = pd.read_csv(clustered_data_path)


##### Merge the datasets #####
# create merged dataset -> match the clusters on the labeled dataset to the input cluster dataset
# merging labeled dataset into the clustered dataset, using the asteroid numbers, keeping only rows that both match (inner)
df_merged = df_clustered.merge(df_labeled, left_on="Name", right_on = "ast_name", how = "inner")


# determine what family each cluster should theoretically be in
cluster_family = df_merged.groupby("cluster_id")["family1"].agg(lambda x: x.value_counts().idxmax())
df_merged["determined_family"] = df_merged["cluster_id"].map(cluster_family)

##### Calculate Family Purity #####
# Purity: how many of the clustered asteroids actually match the family of that cluster?
df_merged_purity = df_merged[df_merged["cluster_id"] >= 0].copy()
df_merged_purity["correct"] = df_merged_purity["family1"] == df_merged_purity["determined_family"]
correct = df_merged_purity["correct"]
wrong = ~df_merged_purity["correct"]

purity = correct.mean()
print(f"Mean cluster Purity: {purity:.2%} (only clustered asteroids considered)")


# plot #
plt.figure()

plt.scatter(
    df_merged_purity.loc[wrong, "a_AU"],
    df_merged_purity.loc[wrong, "sin_I"],
    s=0.2,
    c="lightgray",
    label="Incorrect"
)

plt.scatter(
    df_merged_purity.loc[correct, "a_AU"],
    df_merged_purity.loc[correct, "sin_I"],
    s=0.2,
    c="red",
    label="Correct"
)

plt.xlabel("a (AU)")
plt.ylabel("sin(i)")
plt.legend()
plt.title(f"Clustering Purity (Red = Correct, Gray = Wrong) | Purity = {purity:.2%}")
plt.show()



##### Calculate Family Completeness #####
# Complteness: of all the labeled asteroids, how many were correclty clustered into their fmaily?
# clustered asteroid is only counted as correct if it is both clustered AND the matches the labeled family
df_merged_completeness = df_merged.copy()
df_merged_completeness["correct"] = (
    (df_merged_completeness["cluster_id"] >= 0) &
    (df_merged_completeness["family1"] == df_merged_completeness["determined_family"])
)
# completeness is fraction of all labeled asteroids that are correct
completeness = df_merged_completeness["correct"].mean()
print(f"Cluster Completeness: {completeness:.2%} (all labeled asteroids considered)")


# plot #
correct = df_merged_completeness["correct"]
wrong = ~df_merged_completeness["correct"]

plt.figure()
plt.scatter(
    df_merged_completeness.loc[wrong, "a_AU"],
    df_merged_completeness.loc[wrong, "sin_I"],
    s=0.2,
    c="lightgray",
    label="Incorrect"
)

plt.scatter(
    df_merged.loc[correct, "a_AU"],
    df_merged.loc[correct, "sin_I"],
    s=0.2,
    c="red",
    label="Correct"
)

plt.xlabel("a (AU)")
plt.ylabel("sin(i)")
plt.legend()
plt.title(f"Clustering Completeness (Red = Correct, Gray = Wrong) | Completeness = {completeness:.2%}")
plt.show()


# output table with the cluster numbers, family numbers, and the correctness, sorted from most correct to lowest as an excel spreadsheet
##### Output table #####
# show cluster_id, determined_family, true family, correctness
output_table = df_merged_completeness[[
    "Name", "cluster_id", "determined_family", "family1", "correct"
]].sort_values(by="correct", ascending=False)

output_table.to_excel(base_path + "cluster_validation_correctness.csv", index=False)
