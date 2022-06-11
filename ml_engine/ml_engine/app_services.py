from loguru import logger

from ml_engine.app import engine_provider
from ml_engine.services import EngineProviderService


async def get_engine_provider():
    logger.debug("get_registry_provider")
    return EngineProviderService(engine_provider)
