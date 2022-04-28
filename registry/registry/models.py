import random
import ast
from typing import List

from loguru import logger


class ServiceInstance:
    """It holds data about the instance of a service"""

    def __init__(self, name: str, ip_addresses, ports):
        self.name: str = name
        self.ip_addresses = ip_addresses
        self.ports = ports

    def __repr__(self):
        return f"ServiceInstance [name={self.name}, ip_addresses={self.ip_addresses}, ports={self.ports}]"

    def get_default_port(self):
        for port in self.ports:
            if self.ports[port][0]['PublicPort']:
                return self.ports[port][0]['PublicPort']
        logger.error(f"No port found for this service instance")


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
        logger.debug(
            f"Added instance for {self.name} reachable at {instance.name}.weave.local")

    def get_random_instance(self) -> ServiceInstance:
        if len(self.instances) < 1:
            logger.debug("There aren't instances available for this service")
        return random.choice(self.instances)


class ServiceRegistry:
    """The ServiceRegistry class holds information about all registered services"""

    def __init__(self, name: str):
        self.name = name
        self.inspectors: List[ServiceInspector] = []

    def __repr__(self):
        return f"ServiceRegistry [inspectors={str(self.inspectors)}]"

    def register_inspector(self, inspector: ServiceInspector) -> bool:
        if not self.check_unique_name(inspector.name):
            logger.error(f"Cannot register inspector: name already exists")
            return False
        if not self.check_unique_alias(inspector.aliases):
            logger.error(f"Cannot register inspector: one of the aliases already exists")
            return False
        self.inspectors.append(inspector)
        logger.debug(f"Added inspector: {inspector.name}")
        return True

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

    def search_by_ip_address(self, ip_address: str) -> str:
        """Retrieve a registered service instance name by its ip address"""
        for inspector in self.inspectors:
            for service in inspector.instances:
                for ip in service.ip_addresses:
                    if service.ip_addresses[ip] == ip_address:
                        return service.name

    def search_by_name(self, instance_name: str) -> ServiceInstance:
        """Retrieve a registered service instance name by its ip address"""
        for inspector in self.inspectors:
            for service in inspector.instances:
                if service.name == instance_name:
                    return service


class ContainerStructure:
    """Data definition of a container"""

    def __init__(self, container_id: str, name: str, image: str, ip_addresses, ports):
        self.container_id = container_id
        self.name = name
        self.image = image
        self.ip_addresses = ip_addresses
        self.ports = ports

    def __repr__(self):
        return f"ContainerStructure [container_id={self.container_id}, name={self.name}, image={self.image}, " \
               f"ip_addresses={self.ip_addresses}, ports={self.ports}]"

    @staticmethod
    def parse(structure_entry):
        # str -> dict
        structure_entry = ast.literal_eval(structure_entry)
        new_container = ContainerStructure(structure_entry['ID'],
                                           structure_entry['Name'],
                                           structure_entry['Image'],
                                           structure_entry['IPAddresses'],
                                           structure_entry['Ports'])
        return new_container


class ContainerRegistry:
    """Mantains a set of registered containers that will be monitored"""

    def __init__(self, name: str):
        self.name = name
        self.containers: List[ContainerStructure] = []
        self.registration_complete = False

    def __repr__(self):
        return f"ContainerRegistry [containers={self.containers}"

    def register_container(self, new_container: ContainerStructure) -> bool:

        # check if container already registered
        for c in self.containers:
            if c.name == new_container.name:
                self.registration_complete = True
                return False
        self.containers.append(new_container)
        return True

    def find_all_by_name(self, name):
        _found_containers: List[ContainerStructure] = []

        for container in self.containers:
            if name in container.name:
                _found_containers.append(container)
        return _found_containers
