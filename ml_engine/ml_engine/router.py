import requests
import json

from loguru import logger
from fastapi import APIRouter, Depends

import config
from ml_engine.services import EngineProviderService
from ml_engine.app_services import get_engine_provider

router = APIRouter(
    tags=['ml_engine'],
    prefix=''
)


@router.get('/predict/{service_type}')
async def get_registry(service_type: str, engine_provider: EngineProviderService = Depends(get_engine_provider)):
    """Predictions endpoint. Receiving a json payload of last response times and cpu utilization,
       use the correct model to predict a service performance"""

    engine_provider = engine_provider.get_engine_provider()

    # TODO: CALL MONITORING

    monitoring_response = requests.get(f"http://{config.MONITORING_HOST}/data/{service_type}")
    if monitoring_response.status_code != 200:
        return

    data = monitoring_response.json()
    logger.debug(data)
    data = engine_provider.predict(service_type, data)

    data['pred_rt'] = json.dumps(data['pred_rt'].tolist())
    data['pred_cpu'] = json.dumps(data['pred_cpu'].tolist())
    return data
