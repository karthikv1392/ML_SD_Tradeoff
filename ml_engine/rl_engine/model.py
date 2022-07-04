from collections import namedtuple
from typing import List


SelectionState = namedtuple("SelectionState", "rt_category cpu_category instance")

class CurrentData:
    def __init__(self, type: str, rt_values: List[float], cpu_values: List[float]):
        self.type = type
        self.rt_values = rt_values
        self.cpu_values = cpu_values
