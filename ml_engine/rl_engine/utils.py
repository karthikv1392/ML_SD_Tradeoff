import numpy as np


# explicit function to normalize array
def normalize(array):
    norm = np.linalg.norm(array)
    array = array/norm  # normalized matrix
    return array
