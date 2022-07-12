from time import sleep
from typing import Dict, List

from rl_engine.world import SelectionWorld
from rl_engine.model import SelectionState, CurrentData
from loguru import logger

import rl_engine.services as services
import rl_engine.utils as utils

import ast
import numpy as np


class SelectionEngineRegistry:
    """Registry of the available SelectionEngine"""
    def __init__(self, service_types: List[str]):
        self.selection_engines = {}
        self.rt_categories = ['LOW', 'MED', 'HI']
        self.cpu_categories = ['LOW', 'MED', 'HI']

        for s in service_types:
            available_instances = services.get_available_instances(s)

            selection_world = SelectionWorld(available_instances, self.rt_categories, self.cpu_categories)
            selection_engine = SelectionEngine(s, selection_world)

            self.selection_engines[s] = selection_engine

    def get_selection_enine(self, service_type):
        return self.selection_engines[service_type]


class SelectionEngine:
    """Responsible for maintaining the state of the selection process for a kind of service"""

    def __init__(self,
                 service_type: str,
                 world: SelectionWorld,
                 learning_rate: float = 0.1,
                 discount_f: float = 0.9,
                 epsilon: float = 0.2,
                 adaptive_epsilon: bool = False):

        self.service_type = service_type  # key for the service kind
        self.world: SelectionWorld = world  # the enviromnent that the agent observe and navigates
        self.learning_rate = learning_rate  # how much does the agent take into account the learning error at each step
        self.discount_f = discount_f  # discount factor, i.e. how much weight is given to future rewards
        self.epsilon = epsilon  # epsilon greedy policy, how much the agent try to explore
        self.adaptive_epsilon = adaptive_epsilon

        self.q_table: Dict[(SelectionState, str)] = self.init_q_table()
        self.state: SelectionState = None

    def init_q_table(self) -> Dict[(SelectionState, str)]:
        """Initializes the Q-Table: |s| x |a| with zeros"""
        q_table = {}

        for state in [(rt_c, cpu_c, i) for rt_c in self.world.rt_categories for cpu_c in self.world.cpu_categories
                      for i in self.world.available_instances]:
            for action in self.world.actions:
                q_table[(state, action)] = 0
        return q_table

    def select_action(self, curr_data: CurrentData):
        """Given the current ranking, select the best instance using the q-table"""
        curr_states = self.data_to_states(curr_data)

        if self.state is None:
            action = np.random.choice(self.world.actions)
            self.state = SelectionState(self.world.rt_categories[0], self.world.cpu_categories[0], action)
            logger.debug(f"State has not been initiliazed. Picking random state: {self.state}")
            return action
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(self.world.actions)
            self.state = SelectionState(self.state.rt_category, self.state.cpu_category, action)
            logger.debug(f"Esploring new states (epsilon value): {self.state}")

            return action
        else:
            action = self.max_action(curr_states)
            return action

    def max_action(self, curr_states: List[SelectionState]) -> str:
        """Queries the q-table to extract the current best action, given the current state"""

        q_values = np.array([self.q_table[(self.state, s.instance)] for s in curr_states], dtype=float)
        max_index = q_values.argmax()
        logger.debug(max_index)
        logger.debug(self.world.actions)

        selected_action = self.world.actions[max_index]

        self.post_action(selected_action)
        return selected_action

    def post_action(self, instance):
        """Retrieves live data in order to update the reward table with proper values"""
        data = services.get_current_entry(instance)
        logger.debug(data)

    def data_to_states(self, curr_data: CurrentData) -> List[SelectionState]:

        pred_rt = utils.normalize(curr_data.rt_values).reshape(5)
        pred_cpu = utils.normalize(curr_data.cpu_values).reshape(5)

        curr_states: List[SelectionState] = []

        for index, a in enumerate(self.world.actions):
            if pred_rt[index] < 0.4:
                rt_category = 'LOW'
            elif pred_rt[index] < 0.6:
                rt_category = 'MED'
            else:
                rt_category = 'HI'

            if pred_cpu[index] < 0.4:
                cpu_category = 'LOW'
            elif pred_cpu[index] < 0.6:
                cpu_category = 'MED'
            else:
                cpu_category = 'HI'

            state = SelectionState(rt_category, cpu_category, a)
            curr_states.append(state)

        return curr_states


if __name__ == "__main__":

    service_type = "catalogue"

    available_instances = services.get_available_instances(service_type)

    world = SelectionWorld(available_instances, ['LOW', 'MED', 'HI'], ['LOW', 'MED', 'HI'])

    selection_engine = SelectionEngine(service_type, world)

    raw_test_data = {
        "key": "catalogue",
        "pred_rt": "[[118.9261474609375, 238.39471435546875, 99.03601837158203, 56.91542053222656, 127.10435485839844]]",
        "pred_cpu": "[[0.184543177485466, 0.18001843988895416, 0.07000000029802322, 0.16921639442443848, 0.3747855842113495]]"
    }

    # TODO: call predictor
    test_data = CurrentData(raw_test_data["key"],
                            np.array(ast.literal_eval(raw_test_data['pred_rt'])),
                            np.array(ast.literal_eval(raw_test_data['pred_cpu'])))

    for i in range(5):
        logger.debug(selection_engine.select_action(test_data))
        sleep(1)
