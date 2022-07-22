from typing import Dict, List
from fastapi import BackgroundTasks

from rl_engine.world import SelectionWorld
from rl_engine.model import SelectionState, CurrentData, QoSCategory
from loguru import logger

import rl_engine.services as services
import rl_engine.utils as utils

import numpy as np
import os


class SelectionEngineRegistry:
    """Registry of the available SelectionEngine"""

    def __init__(self, service_types: List[str]):
        self.selection_engines = {}
        self.rt_categories = QoSCategory.get_categories()
        self.cpu_categories = QoSCategory.get_categories()

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

        self.log_file = f"rl_engine/logs/{service_type}.log"
        logger.debug(os.getcwd())
        open(self.log_file, 'w')
        self.service_type = service_type  # key for the service kind
        self.world: SelectionWorld = world  # the enviromnent that the agent observe and navigates
        self.learning_rate = learning_rate  # how much does the agent take into account the learning error at each step
        self.discount_f = discount_f  # discount factor, i.e. how much weight is given to future rewards
        self.epsilon = epsilon  # epsilon greedy policy, how much the agent try to explore
        self.adaptive_epsilon = adaptive_epsilon

        self.q_table: Dict[(SelectionState, str)] = self.init_q_table()
        self.state = None
        self.action = None

    def init_q_table(self) -> Dict[(SelectionState, str)]:
        """Initializes the Q-Table: |s| x |a| with zeros"""
        q_table = {}

        for state in [(rt_c, cpu_c, i) for rt_c in self.world.rt_categories for cpu_c in self.world.cpu_categories
                      for i in self.world.available_instances]:
            for action in self.world.actions:
                q_table[(state, action)] = 0
        return q_table

    def select_action(self, curr_data: CurrentData,
                      background_tasks: BackgroundTasks):
        """Given the current ranking, select the best instance using the q-table"""

        # Explore a random state
        if np.random.uniform(0, 1) < self.epsilon and self.state is not None:
            max_action = np.random.choice(self.world.actions)
            new_state = SelectionState(np.random.choice(QoSCategory.get_categories()),
                                       np.random.choice(QoSCategory.get_categories()), max_action)
            logger.debug(f"Esploring new states (epsilon value): {self.state}")
            max_index = None
        # Select maximizing state
        else:
            curr_states = self.data_to_states(curr_data)
            logger.debug(f"Current states predictions: {curr_states}")
            max_index, max_action, new_state = self.max_action(curr_states)

        # initialize first state and action selected
        if self.state is None:
            self.state = new_state
        if self.action is None:
            self.action = max_action

        background_tasks.add_task(self.post_action, max_action, new_state, self.action, self.state, curr_data, max_index)

        self.state = new_state
        self.action = max_action

        return max_action

    def max_action(self, curr_states: List[SelectionState]) -> (str, float, SelectionState):
        """Queries the q-table to extract the current best action, given the current state"""
        q_values = np.array([self.q_table[(s, s.instance)] for s in curr_states], dtype=float)
        max_index = q_values.argmax()
        max_value = q_values.max()

        max_action = self.world.actions[max_index]
        logger.debug(f"max_action - selected action: '{max_action}',  having the max q_value: '{max_value}'")

        new_state = curr_states[max_index]

        logger.debug(f"max_action - new state is: {new_state}")

        return max_index, max_action, new_state

    def post_action(self, max_action: str, new_state: SelectionState,
                    old_action: str, old_state: SelectionState, curr_data: CurrentData, max_index: int):
        """Retrieves live data in order to update the reward table with proper values"""
        logger.debug(f"post_action - current state: {self.state}")
        data = services.get_current_entry(max_action)

        logger.debug(f"post_action - current data: {data}")

        rt, cpu = float(data['rt']), float(data['cpu'])

        if max_index is not None:
            pred_rt = curr_data.rt_values.reshape(5)[max_index]
            pred_cpu = curr_data.cpu_values.reshape(5)[max_index]
        else:
            pred_rt = "Nan"
            pred_cpu = "Nan"
        rt_array = np.concatenate([curr_data.rt_values.reshape(5), np.array([rt])])
        cpu_array = np.concatenate([curr_data.cpu_values.reshape(5), np.array([cpu])])

        rt_array = utils.normalize(rt_array)
        cpu_array = utils.normalize(cpu_array)

        curr_rt = rt_array[-1]
        curr_cpu = cpu_array[-1]

        logger.debug(f"post_action - {curr_rt}")
        logger.debug(f"post_action - {curr_cpu}")

        rt_category = QoSCategory.category_by_value(curr_rt)

        cpu_category = QoSCategory.category_by_value(curr_cpu)

        effective_state = SelectionState(rt_category, cpu_category, max_action)
        logger.debug(f"post_action - effective_state: {effective_state}")
        reward = self.give_reward(new_state, effective_state)


        #  Q(state, action) <- (1 - learning_rate) Q(state, action) + learning_rate (reward + discount maxQ(next_state, all_actions))
        new_value = (1 - self.learning_rate) * self.q_table[(old_state, old_action)] + self.learning_rate * (reward + self.discount_f * self.q_table[(new_state, max_action)])
        logger.debug(f"Formula 1: {new_value}")

        self.q_table[(old_state, old_action)] = new_value

        with open(self.log_file, 'a') as log:
            log.write(f"{{'state': {old_state}, 'action': {old_action}, 'selected_state': {new_state}, 'max_action': {max_action}, 'gross_reward': {reward}, 'new_q_value': {new_value}, 'pred_rt': {pred_rt}, 'curr_rt': {rt}, 'pred_cpu': {pred_cpu}, 'curr_cpu': {cpu} }} \n")
        logger.debug(f"post_action - reward: {reward}")
        logger.debug(f"post_action - updated q_value: q_table[({new_state}, {max_action})]: {new_value}")

    def give_reward(self, selected_state, effective_state) -> float:
        rt_delta = selected_state.rt_category - effective_state.rt_category
        cpu_delta = selected_state.cpu_category - effective_state.cpu_category
        x, y = 1, 1
        return x * rt_delta + y * cpu_delta

    def data_to_states(self, curr_data: CurrentData) -> List[SelectionState]:

        pred_rt = utils.normalize(curr_data.rt_values).reshape(5)
        pred_cpu = utils.normalize(curr_data.cpu_values).reshape(5)

        curr_states: List[SelectionState] = []

        for index, a in enumerate(self.world.actions):
            rt_category = QoSCategory.category_by_value(pred_rt[index])

            cpu_category = QoSCategory.category_by_value(pred_cpu[index])

            state = SelectionState(rt_category, cpu_category, a)
            curr_states.append(state)
        logger.debug(f"Current '{self.service_type}' instances data: {curr_states}")
        return curr_states
