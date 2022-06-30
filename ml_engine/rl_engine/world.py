from typing import List, Dict
from state import SelectionState
from loguru import logger


class SelectionWorld:
    """The world in which the SelectionAgent moves between different stases.
       Here we define the world dimensions, how the world can be explored and its limits."""

    def __init__(self, available_instances: List[str], rt_categories: List[str], cpu_categories: List[str]):
        self.available_instances = available_instances
        self.rt_categories = rt_categories
        self.cpu_categories = cpu_categories

        # TODO: DEFINE ACTIONS
        self.actions = available_instances

        # TODO: DEFINE REWARD TABLE r(s) = reward_value
        self.rewards = self.init_rewards()

    def next_state(self, state: SelectionState, action: str) -> SelectionState:
        """Generate the state s' from chosing action a in state s"""
        # TODO: DEFINE HOW EACH ACTION CHANGES CURRENT STATE INTO S'
        if action not in self.available_instances:
            logger.error(f"Action '{action}' is invalid")
        return SelectionState('', '', '')

    def init_rewards(self) -> Dict[SelectionState, float]:
        """Initalize the rewards table"""
        # TODO
        rewards: Dict[(str, str, str), float] = {}

        for state in [(rt_c, cpu_c, i) for rt_c in self.rt_categories for cpu_c in self.cpu_categories
                      for i in self.available_instances]:
            s = SelectionState(state[0], state[1], state[2])
            rewards[s] = 0

            # TODO: REWARDS TUNING BASED ON CATEGORIES VALUES

        return rewards
