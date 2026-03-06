"""
Converts .txt dataset into usable .csv file that will run with the machine learning algorithms.
"""

import pandas as pd

base_path = "/mnt/c/Users/amineeva/OneDrive - Olin College of Engineering/2025-2026/Semester 2/Scientific Computing/Project 2 - Asteroids/"
# asteroid_data_download_path = base_path + "Synthetic_Proper_Elements_Hirayama_full_dataset.txt"
# asteroid_data_output_path = base_path + "Synthetic_Proper_Elements_Hirayama_full_dataset.csv"

asteroid_data_download_path = base_path + "all_tro.members.txt"
asteroid_data_output_path = base_path + "all_tro.members.csv"

# Column names
# columns = [
#     "Name",
#     "mag",
#     "a_AU",
#     "e",
#     "sin_I",
#     "n_deg_per_yr",
#     "g_arcsec_per_yr",
#     "s_arcsec_per_yr",
#     "LCEx1E6",
#     "My"
# ]
columns = [
  "ast_name",
  "Hmag",
  "status",
  "family1",
  "dv_fam1",
  "near1",
  "family2",
  "dv_fam2",
  "near2",
  "rescod"
  ]


# Convert downloaded .txt file stored locally to .csv file
df = pd.read_csv(
    asteroid_data_download_path,
    comment="%",
    delim_whitespace=True,
    names=columns
)

# Debugging output print of dataset
# print(df.head())

# Save the dataset to a .csv locally
df.to_csv(asteroid_data_output_path, index=False)