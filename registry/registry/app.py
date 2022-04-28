from fastapi import FastAPI
from loguru import logger

from registry.core import ServiceRegistryProvider

# init containers inspection
logger.debug("app, initializing registry_provider")
registry_provider = ServiceRegistryProvider()

from .router import router as main_router

app = FastAPI(
    title="Service Registry",
    description="",
    version="0.0.1"
)

app.include_router(main_router)
