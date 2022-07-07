import requests
from asgiref.sync import async_to_sync

import pandas as pd
from .config import DMON_STRUCTURE_TOPIC, DMON_NETWORK_TOPIC
from .redis_client import init_redis_client, get_subscriber
from loguru import logger
import ast
import monitoring.config as config
from .tables import ServiceCall, ServiceStatus, LiveServiceCall, LiveServiceStatus
import monitoring.services as services
from datetime import datetime, timedelta


def extract_call(data, live=False):
    if data["Protocol"] != "HTTP/JSON" and data["Protocol"] != "HTTP":
        return
    ip = data['SendIP']
    registry_response = requests.get(f"http://{config.REGISTRY_HOST}/services/by-ip/{ip}")

    if registry_response.status_code != 200:
        # logger.debug(f"No service instance found for ip {ip}")
        return
    registry_response = registry_response.json()

    if live:
        ts = pd.to_datetime(data['Timestamp']) + timedelta(hours=2)
        live_service_call: LiveServiceCall = LiveServiceCall(timestamp=ts,
                                                             time_delta=data['TimeDelta'],
                                                             service_instance=registry_response['name'],
                                                             service_type=registry_response['type'])
        services.store_live_service_call(live_service_call)
        return

    service_call: ServiceCall = ServiceCall(timestamp=data['Timestamp'],
                                            time_delta=data['TimeDelta'],
                                            service_instance=registry_response['name'],
                                            service_type=registry_response['type'])

    services.store_service_call(service_call)


def extract_status(data, live=False):
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

    if live:

        ts = pd.to_datetime(data['Timestamp']) + timedelta(hours=2)

        live_service_status: LiveServiceStatus = LiveServiceStatus(timestamp=ts,
                                                                   cpu_perc=cpu_perc,
                                                                   service_instance=service_name,
                                                                   service_type=service_type)

        services.store_live_service_status(live_service_status)
        return

    service_status: ServiceStatus = ServiceStatus(timestamp=data['Timestamp'],
                                                  cpu_perc=cpu_perc,
                                                  service_instance=service_name,
                                                  service_type=service_type)

    services.store_service_status(service_status)


class RedisMonitor:
    def __init__(self):
        self.redis_client = init_redis_client()

    def start_monitoring(self, topic, live=False):
        sub = get_subscriber(self.redis_client, topic)

        try:

            for entry in sub.listen():
                if entry['data'] == 1:
                    continue  # skip init data
                data = ast.literal_eval(entry['data'].decode())

                if topic == DMON_NETWORK_TOPIC:
                    extract_call(data, live)
                elif topic == DMON_STRUCTURE_TOPIC:
                    extract_status(data, live)

        except ConnectionError:
            logger.debug("Restarting monitoring..")
            self.start_monitoring(topic)

    def test(self, topic):
        sub = get_subscriber(self.redis_client, topic)
        for entry in sub.listen():
            logger.debug(entry)


def live(topic):
    service_monitor = RedisMonitor()
    service_monitor.start_monitoring(topic, live=True)
