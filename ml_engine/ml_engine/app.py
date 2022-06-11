from fastapi import FastAPI
from loguru import logger

from ml_engine.core import EngineProvider

# init containers inspection
logger.debug("app, initializing registry_provider")
engine_provider = EngineProvider()

from ml_engine.router import router as main_router

app = FastAPI(
    title="ML engine service",
    description="",
    version="0.0.1"
)

app.include_router(main_router)
