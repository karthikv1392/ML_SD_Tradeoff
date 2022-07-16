from time import sleep
from typing import Dict, List
from fastapi import BackgroundTasks

from ml_engine.core import PredictionEngine
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

    def get_selection_engine(self, service_type):
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

    def select_action(self, curr_data: CurrentData, prediction_engine: PredictionEngine,
                      background_tasks: BackgroundTasks):
        """Given the current ranking, select the best instance using the q-table"""
        curr_states = self.data_to_states(curr_data, prediction_engine)

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
            max_action, max_value, selected_state = self.max_action(curr_states)
            background_tasks.add_task(self.post_action, max_action, max_value, selected_state, curr_data)

            return max_action

    def max_action(self, curr_states: List[SelectionState]) -> (str, float, SelectionState):
        """Queries the q-table to extract the current best action, given the current state"""
        q_values = np.array([self.q_table[(self.state, s.instance)] for s in curr_states], dtype=float)
        max_index = q_values.argmax()
        max_value = q_values.max()

        logger.debug(f"max_action - max_index: {max_index}")

        max_action = self.world.actions[max_index]
        selected_state = curr_states[max_index]

        self.state = selected_state

        return max_action, max_value, selected_state

    def post_action(self, max_action: str, max_value: float, new_state: SelectionState, curr_data: CurrentData):
        """Retrieves live data in order to update the reward table with proper values"""
        logger.debug(f"post_action - current state: {self.state}")
        data = services.get_current_entry(max_action)

        logger.debug(f"post_action - current data: {data}")

        # TODO: update q_table
        rt, cpu = float(data['rt']), float(data['cpu'])

        rt_array = np.concatenate([curr_data.rt_values.reshape(5), np.array([rt])])
        cpu_array = np.concatenate([curr_data.cpu_values.reshape(5), np.array([cpu])])

        rt_array = utils.normalize(rt_array)
        cpu_array = utils.normalize(cpu_array)

        curr_rt = rt_array[-1]
        curr_cpu = cpu_array[-1]

        logger.debug(f"post_action - {curr_rt}")
        logger.debug(f"post_action - {curr_cpu}")

        if curr_rt < 0.4:
            rt_category = 'LOW'
        elif curr_rt < 0.6:
            rt_category = 'MED'
        else:
            rt_category = 'HI'

        if curr_cpu < 0.4:
            cpu_category = 'LOW'
        elif curr_cpu < 0.6:
            cpu_category = 'MED'
        else:
            cpu_category = 'HI'

        if rt_category == new_state.rt_category:
            reward = 1

        # delta = reward(next_state) + discount * q_table(next_state, next_action) - q_table(past_state, past_action)
        # q_table(next_state, next_action) += learning_rate * delta

    def give_reward(self, state):
        # prediction vs real value and calculate a reward
        pass

    def data_to_states(self, curr_data: CurrentData, prediction_engine: PredictionEngine) -> List[SelectionState]:

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
        logger.debug(f"Current '{self.service_type}' instances data: {curr_states}")
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
