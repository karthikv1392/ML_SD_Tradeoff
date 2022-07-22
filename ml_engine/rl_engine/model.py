from collections import namedtuple
import numpy as np

SelectionState = namedtuple("SelectionState", "rt_category cpu_category instance")


class CurrentData:
    def __init__(self, key: str, rt_values: np.ndarray, cpu_values: np.ndarray):
        self.key = key
        self.rt_values = rt_values
        self.cpu_values = cpu_values


class QoSCategory:
    LOW = 0
    MED = 1
    HI = 2

    @classmethod
    def get_categories(cls):
        return [cls.LOW, cls.MED, cls.HI]

    @classmethod
    def category_by_value(cls, value: float):

        if value < 0 or value > 1:
            raise ValueError

        if value < 0.4:
            return cls.LOW

        if value < 0.6:
            return cls.MED

        return cls.HI
