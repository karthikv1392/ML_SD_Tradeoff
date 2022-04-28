from loguru import logger

from registry.core import ServiceRegistryProvider


class RegistryProviderService:
    def __init__(self, registry_provider: ServiceRegistryProvider):
        logger.debug("MonitoringService __init__")
        self.registry_provider = registry_provider

    def get_registry_provider(self):
        logger.debug("MonitoringService get_registry")
        return self.registry_provider
