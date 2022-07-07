from collections import namedtuple
from typing import List
import numpy as np

SelectionState = namedtuple("SelectionState", "rt_category cpu_category instance")


class CurrentData:
    def __init__(self, key: str, rt_values: np.ndarray, cpu_values: np.ndarray):
        self.key = key
        self.rt_values = rt_values
        self.cpu_values = cpu_values
