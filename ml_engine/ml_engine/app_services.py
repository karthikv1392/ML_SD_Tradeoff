from loguru import logger

from ml_engine.app import prediction_engine
from ml_engine.services import PredictionEngineProvider, SelectionEngineRegistryProvider
from ml_engine.app import selection_engine_registry


async def get_prediction_engine_provider():
    logger.debug("get_prediction_engine_provider")
    return PredictionEngineProvider(prediction_engine)


async def get_selection_engine_registry_provider():
    logger.debug("get_selection_engine_provider")
    return SelectionEngineRegistryProvider(selection_engine_registry)
