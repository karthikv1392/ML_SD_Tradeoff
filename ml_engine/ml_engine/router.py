from typing import Dict

from loguru import logger
from fastapi import APIRouter, Request, Response, Depends, HTTPException

from ml_engine.services import EngineProviderService
from ml_engine.app_services import get_engine_provider

router = APIRouter(
    tags=['ml_engine'],
    prefix=''
)


@router.get('/engines')
async def get_registry(engine_provider: EngineProviderService = Depends(get_engine_provider)):
    """Predictions endpoint"""

    engine_provider = engine_provider.get_engine_provider()

    return "Pippo"
