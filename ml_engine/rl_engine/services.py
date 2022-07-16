import requests
from loguru import logger
import rl_engine.config as config
from typing import List
from datetime import datetime


def get_available_instances(service_type: str) -> List[str]:
    available_instances_response = requests.get(f"http://{config.REGISTRY_HOST}/services/{service_type}/instances")

    if available_instances_response.status_code != 200:
        logger.error(f"No instances found for type {service_type}")

    available_instances = available_instances_response.json()
    available_instances.sort()

    logger.debug(available_instances)

    return available_instances


def get_current_entry(instance: str):
    params = {"timestamp": str(datetime.today())}

    current_entry_response = requests.get(f"http://{config.MONITORING_HOST}/data/single/{instance}", params=params)

    logger.debug(f"Monitoring single current data response: {current_entry_response}")
    current_entry_value = current_entry_response.json()

    return current_entry_value
