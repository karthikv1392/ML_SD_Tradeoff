from monitoring.config import DMON_NETWORK_TOPIC, DMON_STRUCTURE_TOPIC
from monitoring.core import RedisMonitor
import argparse
from loguru import logger

parser = argparse.ArgumentParser()
parser.add_argument("--m", type=str)

args = parser.parse_args()

service_monitor = RedisMonitor()

if args.m == "response_time":
    service_monitor.start_monitoring(DMON_NETWORK_TOPIC)
elif args.m == "cpu_utilization":
    service_monitor.start_monitoring(DMON_STRUCTURE_TOPIC)
else:
    logger.debug("Invalid value for arg --m")
