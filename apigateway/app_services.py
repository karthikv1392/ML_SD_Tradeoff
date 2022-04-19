from loguru import logger

from .app import main_registry
from .services import MonitoringService


async def get_main_service_registry():
    logger.debug("get_main_service_registry")
    return MonitoringService(main_registry)
