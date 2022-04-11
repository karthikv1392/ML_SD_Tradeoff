from loguru import logger
from fastapi import FastAPI

import edge_router.router

app = FastAPI(
    title="Dummy",
    description="",
    version="0.0.1"
)


app.include_router(edge_router.router.router)

