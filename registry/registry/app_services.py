from loguru import logger

from registry.app import registry_provider
from registry.services import RegistryProviderService


async def get_registry_provider():
    logger.debug("get_registry_provider")
    return RegistryProviderService(registry_provider)
