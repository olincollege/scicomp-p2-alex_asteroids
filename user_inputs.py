"""Contains user inputs parameters for all files in asteroid clustering."""

##### imports #####
import numpy as np


##### Clustering parameter values #####
# a (semi-major axis)
a_AU_min = 2.5 #2
a_AU_max = 3.3 #3.5
# a_AU_min = 2.825
# a_AU_max = 2.958

# e (eccentricity)
e_min = 0
e_max = 0.5

# sin(i) (Inclination)
sin_I_min = 0
sin_I_max = np.sin(np.radians(20))