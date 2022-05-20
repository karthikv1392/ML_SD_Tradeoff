import requests
from redis.connection import SERVER_CLOSED_CONNECTION_ERROR

from .config import DMON_STRUCTURE_TOPIC, DMON_NETWORK_TOPIC
from .redis_client import init_redis_client, get_subscriber
from loguru import logger
import ast
import monitoring.config as config
from .tables import ServiceCall, ServiceStatus
import monitoring.services as services


def extract_call(data):
    if data["Protocol"] != "HTTP/JSON" and data["Protocol"] != "HTTP":
        return
    ip = data['SendIP']
    registry_response = requests.get(f"http://{config.REGISTRY_HOST}/services/by-ip/{ip}")

    if registry_response.status_code != 200:
        # logger.debug(f"No service instance found for ip {ip}")
        return
    registry_response = registry_response.json()

    service_call: ServiceCall = ServiceCall(timestamp=data['Timestamp'],
                                            time_delta=data['TimeDelta'],
                                            service_instance=registry_response['name'],
                                            service_type=registry_response['type'])

    services.store_service_call(service_call)


def extract_status(data):
    if data["SubType"] != "container":
        return

    service_name: str = data['Name']
    service_name = service_name.replace('/', '')

    # storing only registered services
    registry_response = requests.get(f"http://{config.REGISTRY_HOST}/services/by-name/{service_name}")
    if registry_response.status_code != 200:
        return

    registry_response = registry_response.json()

    service_type = registry_response['type']

    cpu_perc: str = data['CPUPerc']
    cpu_perc = cpu_perc.replace('%', '')
    service_status: ServiceStatus = ServiceStatus(timestamp=data['Timestamp'],
                                                  cpu_perc=cpu_perc,
                                                  service_instance=service_name,
                                                  service_type=service_type)

    services.store_service_status(service_status)


class RedisMonitor:
    def __init__(self):
        self.redis_client = init_redis_client()

    def start_monitoring(self, topic):
        sub = get_subscriber(self.redis_client, topic)

        try:

            for entry in sub.listen():
                if entry['data'] == 1:
                    continue  # skip init data
                data = ast.literal_eval(entry['data'].decode())

                if topic == DMON_NETWORK_TOPIC:
                    extract_call(data)
                elif topic == DMON_STRUCTURE_TOPIC:
                    extract_status(data)

        except ConnectionError:
            logger.debug("Restarting monitoring..")
            self.start_monitoring(topic)

    def test(self, topic):
        sub = get_subscriber(self.redis_client, topic)
        for entry in sub.listen():
            logger.debug(entry)

