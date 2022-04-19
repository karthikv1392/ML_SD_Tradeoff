from loguru import logger


class MonitoringService:
    def __init__(self, registry):
        logger.debug("MonitoringService __init__")
        self.registry = registry

    def get_main_registry(self):
        logger.debug("MonitoringService get_registry")
        return self.registry
