from fastapi import HTTPException
from loguru import logger

from ml_engine.core import PredictionEngine
from rl_engine.core import SelectionEngineRegistry
import requests
from rl_engine import config
import json


class PredictionEngineProvider:
    def __init__(self, prediction_engine: PredictionEngine):
        logger.debug("PredictionEngineProvider __init__")
        self.prediction_engine = prediction_engine

    def get_prediction_engine(self):
        logger.debug("PredictionEngine: get_prediction_engine")
        return self.prediction_engine


class SelectionEngineRegistryProvider:
    def __init__(self, selection_engine_registry: SelectionEngineRegistry):
        logger.debug("SelectionEngineRegistryProvider __init__")
        self.selection_engine_registry_provider = selection_engine_registry

    def get_selection_engine_registry(self):
        logger.debug("SelectionEngineRegistryProvider get_selection_engine_registry")
        return self.selection_engine_registry_provider


def get_predictions(service_type: str, prediction_engine: PredictionEngine):

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
