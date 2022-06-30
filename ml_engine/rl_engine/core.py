from typing import Dict

from agent import SelectionAgent
from world import SelectionWorld
from state import SelectionState
from loguru import logger

import requests
import config


class SelectionEngineProvider:
    """Responsible for maintaining the state of the selection process for a kind of service"""
    def __init__(self,
                 service_type: str,
                 agent: SelectionAgent,
                 world: SelectionWorld,
                 learning_rate: float = 0.1,
                 discount_f: float = 0.9,
                 epsilon: float = 0.2,
                 adaptive_epsilon: bool = False):

        self.service_type = service_type  # key for the service kind
        self.agent: SelectionAgent = agent  # the agent that is performing a selection
        self.world: SelectionWorld = world  # the enviromnent that the agent observe and navigates
        self.learning_rate = learning_rate  # how much does the agent take into account the learning error at each step
        self.discount_f = discount_f  # discount factor, i.e. how much weight is given to future rewards
        self.epsilon = epsilon  # epsilon greedy policy, how much the agent try to explore
        self.adaptive_epsilon = adaptive_epsilon

        self.qtable: Dict[(SelectionState, str)] = {}

        available_instances_response = requests.get(f"http://{config.REGISTRY_HOST}/services/{service_type}/all")

        if available_instances_response.status_code != 200:
            logger.error(f"No instances found for type {type}")
            return

        available_instances = available_instances_response.json()
