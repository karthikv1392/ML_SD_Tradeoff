class SelectionState:
    """Representation of a state in the SelectionWorld"""
    def __init__(self, rt_category: str, cpu_category: str, instance: str):
        self.rt_category = rt_category
        self.cpu_category = cpu_category
        self.instance = instance
