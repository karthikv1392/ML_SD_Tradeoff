from fastapi import FastAPI
from loguru import logger
from rl_engine import config
from ml_engine.core import PredictionEngine
from rl_engine.core import SelectionEngineRegistry

logger.debug("app, initializing selection engine")
selection_engine_registry = SelectionEngineRegistry(config.services)

logger.debug("app, initializing prediction engine")
prediction_engine = PredictionEngine()


from ml_engine.router import router as main_router

app = FastAPI(
    title="ML engine service",
    description="",
    version="0.0.1"
)

app.include_router(main_router)
