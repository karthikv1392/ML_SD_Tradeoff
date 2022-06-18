from monitoring.router import router as main_router
from fastapi import FastAPI

app = FastAPI(
    title="Monitoring service",
    description="",
    version="0.0.1"
)

app.include_router(main_router)
