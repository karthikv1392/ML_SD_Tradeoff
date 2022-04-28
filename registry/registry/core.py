import yaml

from .redis_client import init_redis_client, get_subscriber
from .config import DMON_STRUCTURE_TOPIC
from loguru import logger
import registry.utils as utils

from .models import ServiceRegistry, ServiceInspector, ServiceInstance, ContainerRegistry,\
    ContainerStructure


class ServiceRegistryProvider:
    def __init__(self):

        self.service_registry = ServiceRegistry('main_service_registry')

        redis_client = init_redis_client()

        # sub to structure topic
        structure_sub = get_subscriber(redis_client, DMON_STRUCTURE_TOPIC)
        container_registry = ContainerRegistry("container_registry")

        # registration phase
        logger.info(f"Containers registration phase started")
        for entry in structure_sub.listen():
            if entry is not None:
                if entry['data'] != 1:  # skip init data
                    # deconding and parsing bytestring
                    result = container_registry.register_container(ContainerStructure.parse(entry['data'].decode()))
                    if not result:
                        break
        logger.info(f"Containers registration completed. Found {len(container_registry.containers)} containers.")

        # service binding phase

        logger.info(f"Services registration phase started")
        # fetch yaml configuration
        with open("config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.Loader)
        # match services name with containers
        for service in cfg:
            logger.debug(f"Binding {service}")
            found_containers = container_registry.find_all_by_name(service)

            if len(found_containers) > 0:
                logger.debug(f"Found {len(found_containers)} instances for {service}")
                service_inspector = ServiceInspector(service, cfg[service]['aliases'])

                for container in found_containers:
                    service_name = utils.remove_char(container.name, '/')
                    service_instance = ServiceInstance(service_name, container.ip_addresses, container.ports)
                    service_inspector.register_instance(service_instance)

                self.service_registry.register_inspector(service_inspector)

        # end binding phase
        logger.info(f"Services registration completed")

    def get_registry_instance(self):
        return self.service_registry
