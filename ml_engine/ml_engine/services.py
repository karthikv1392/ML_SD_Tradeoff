from loguru import logger

from ml_engine.core import EngineProvider


class EngineProviderService:
    def __init__(self, engine_provider: EngineProvider):
        logger.debug("MonitoringService __init__")
        self.engine_provider = engine_provider

    def get_engine_provider(self):
        logger.debug("MonitoringService get_registry")
        return self.engine_provider
