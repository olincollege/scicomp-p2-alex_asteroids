
import pandas as pd

base_path = "/mnt/c/Users/amineeva/OneDrive - Olin College of Engineering/2025-2026/Semester 2/Scientific Computing/Project 2 - Asteroids/"
validation_data_path = base_path + "all_tro.members.csv"
df_labeled = pd.read_csv(validation_data_path)
print(df_labeled["family1"].value_counts())


# returning values of r = 0.0018 ball_tree top 8 (ball tree and kd tree)
print((df_labeled["family1"] == 606).sum())
print((df_labeled["family1"] == 396).sum())
print((df_labeled["family1"] == 3815).sum())
print((df_labeled["family1"] == 1189).sum())
print((df_labeled["family1"] == 1547).sum())
print((df_labeled["family1"] == 3).sum())
print((df_labeled["family1"] == 618).sum())
print((df_labeled["family1"] == 293).sum())
