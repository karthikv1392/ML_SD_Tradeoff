from fastapi import HTTPException
from loguru import logger
import requests
from registry.core import ServiceRegistryProvider
from registry import config


class RegistryProviderService:
    def __init__(self, registry_provider: ServiceRegistryProvider):
        logger.debug("MonitoringService __init__")
        self.registry_provider = registry_provider

    def get_registry_provider(self):
        logger.debug("MonitoringService get_registry")
        return self.registry_provider


def get_tradeoff_instance(service_type: str) -> str:
    tradeoff_instance_response = requests.get(f"http://{config.ML_ENGINE_HOST}/select/{service_type}")

    logger.debug(tradeoff_instance_response)
    tradeoff_instance = tradeoff_instance_response.json()
    if tradeoff_instance_response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find any instance for service type '{service_type}'",
        )

    logger.debug(tradeoff_instance)

    return tradeoff_instance
