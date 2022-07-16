import requests
import json

from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from rl_engine import config
from ml_engine.services import PredictionEngineProvider, SelectionEngineRegistryProvider
from ml_engine.app_services import get_prediction_engine_provider, get_selection_engine_registry_provider
from ml_engine import services
from rl_engine.model import CurrentData
import numpy as np
import ast

router = APIRouter(
    tags=['ml_engine'],
    prefix=''
)


@router.get('/predict/{service_type}')
async def get_predictions(service_type: str, prediction_engine_provider: PredictionEngineProvider = Depends(
    get_prediction_engine_provider)):
    """Predictions endpoint. Receiving a json payload of last response times and cpu utilization,
       use the correct model to predict a service performance"""

    prediction_engine = prediction_engine_provider.get_prediction_engine()

    monitoring_response = requests.get(f"http://{config.MONITORING_HOST}/data/{service_type}")
    if monitoring_response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail=f"Not enough current data is available.",
        )

    data = monitoring_response.json()
    logger.debug(data)
    data = prediction_engine.predict(service_type, data)

    data['pred_rt'] = json.dumps(data['pred_rt'].tolist())
    data['pred_cpu'] = json.dumps(data['pred_cpu'].tolist())
    return data


@router.get('/select/{service_type}')
async def get_selection(service_type: str,
                        background_tasks: BackgroundTasks,
                        prediction_engine_provider: PredictionEngineProvider = Depends(get_prediction_engine_provider),
                        selection_engine_registry_provider: SelectionEngineRegistryProvider = Depends(
                            get_selection_engine_registry_provider),

                        ):
    """Queries the selection engine to retrieve the best next instance, after inspecting the current
       predictions and q_values"""
    prediction_engine = prediction_engine_provider.get_prediction_engine()
    selection_engine_registry = selection_engine_registry_provider.get_selection_engine_registry()

    selection_engine = selection_engine_registry.get_selection_engine(service_type)

    # TODO: retrieve predictions
    predictions = services.get_predictions(service_type, prediction_engine)

    # TODO: do selection
    curr_predicted_data = CurrentData(predictions["key"], np.array(ast.literal_eval(predictions['pred_rt'])), np.array(ast.literal_eval(predictions['pred_cpu'])))
    instance = selection_engine.select_action(curr_predicted_data, prediction_engine, background_tasks)

    return instance
