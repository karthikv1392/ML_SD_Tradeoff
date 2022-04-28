from fastapi import FastAPI
from loguru import logger

from .router import router as main_router

app = FastAPI(
    title="Machine Learning Service Discovery",
    description="",
    version="0.0.1"
)

app.include_router(main_router)
