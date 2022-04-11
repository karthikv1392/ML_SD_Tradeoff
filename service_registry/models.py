import random
from typing import List
from loguru import logger
import yaml


class ServiceInstance:
    """It holds data about the instance of a service"""

    def __init__(self, name: str, host: str, port: str):
        self.name: str = name
        self.host: str = host
        self.port: str = port

    def __repr__(self):
        return f"ServiceInstance [name={self.name}, host={self.host}, port={self.port}]"


class ServiceInspector:
    """The ServiceInspector class manages the instances of a service; it can be queried to retrieve an instance"""

    def __init__(self, name: str, aliases: List[str]):
        logger.debug(f"Inspector '{name}' instantiated")
        self.name: str = name
        self.aliases: List[str] = aliases
        self.instances: List[ServiceInstance] = []

    def __repr__(self):
        return f"ServiceInspector [name={self.name}, aliases={self.aliases}, instances={str(self.instances)}]"

    def register_instance(self, instance: ServiceInstance):
        self.instances.append(instance)
        logger.debug(f"Added instance for {self.name} reachable at {instance.host}:{instance.port}")

    def get_random_instance(self) -> ServiceInstance:
        if len(self.instances) < 1:
            logger.debug("There aren't instances available for this service")
        return random.choice(self.instances)


class ServiceRegistry:
    """The ServiceRegistry class holds information about all registered services"""

    def __init__(self):
        logger.debug("New registry instantiated")
        self.inspectors: List[ServiceInspector] = []
        with open("config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.Loader)

        for service in cfg:
            self.register_inspector(self.read_service(cfg[service]))

    def __repr__(self):
        return f"ServiceRegistry [inspectors={str(self.inspectors)}]"

    def register_inspector(self, inspector: ServiceInspector):
        if not self.check_unique_name(inspector.name):
            logger.error(f"Cannot register inspector: name already exists")

        if not self.check_unique_alias(inspector.aliases):
            logger.error(f"Cannot register inspector: one of the aliases already exists")

        self.inspectors.append(inspector)
        logger.debug(f"Added inspector: {inspector.name}")

    def retrieve_inspector_by_alias(self, alias: str) -> ServiceInspector or None:
        """Query the registry for a matching alias"""
        for inspector in self.inspectors:
            for a in inspector.aliases:
                if a == alias:
                    return inspector
        logger.debug(f"No inspectors found for alias {alias}")

    def check_unique_alias(self, aliases: List[str]) -> bool:
        """Checks if there arleady is an inspector for a new alias. In that case the inspector cannot be registered"""
        for new_alias in aliases:
            for inspector in self.inspectors:
                for alias in inspector.aliases:
                    if new_alias == alias:
                        return False
        return True

    def check_unique_name(self, new_name: str) -> bool:
        """Checks if there already is a service for a new name. In that case the inspector cannot be registered"""
        for inspector in self.inspectors:
            if new_name == inspector.name:
                return False
        return True

    def read_service(self, service) -> ServiceInspector:
        """Create the ServiceInspector from the yml"""
        new_service_inspector = ServiceInspector(service["name"], service["aliases"])
        for key, instance in service["instances"].items():
            new_service_inspector.register_instance(self.read_instance(key, instance))
        return new_service_inspector

    def read_instance(self, key, instance) -> ServiceInstance:
        """Create the ServiceInstance from the yml"""
        new_service_instance = ServiceInstance(key, instance["host"], instance["port"])
        return new_service_instance


# testing
if __name__ == "__main__":
    catalogue_inspector: ServiceInspector = ServiceInspector("catalogue_inspector", ["catalogue"])
    catalogue_inspector.register_instance(ServiceInstance("1", "localhost", "8051"))
    catalogue_inspector.register_instance(ServiceInstance("2", "localhost", "8052"))
    catalogue_inspector.register_instance(ServiceInstance("3", "localhost", "8053"))

    selected_instance = catalogue_inspector.get_random_instance()
    logger.debug(f"Instance selected for {catalogue_inspector.name}: \
                {selected_instance.host}:{selected_instance.port}")
