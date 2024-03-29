import requests

from loguru import logger
from fastapi import APIRouter, Request, Response, HTTPException

import apigateway.utils as utils
import apigateway.config as config

router = APIRouter(
    tags=['apigateway'],
    prefix=''
)


@router.api_route('/{full_path:path}', methods=["GET", "POST", "PUT", "DELETE"])
async def get_interceptor(request: Request):
    # retrieve request info
    info = {"method": request.method,
            "path": request.url.path,
            "headers": request.headers,
            "query_params": request.query_params,
            "body": await request.body(),
            }

    # RANDOM RETRIEVE
    alias: str = utils.get_alias_by_path(info['path'])

    instance_response = None

    if config.LB_STRATEGY == 'rr':
        instance_response = requests.get(f"http://{config.REGISTRY_HOST}/services/{alias}/rr")
    elif config.LB_STRATEGY == 'random':
        instance_response = requests.get(f"http://{config.REGISTRY_HOST}/services/{alias}")
    elif config.LB_STRATEGY == 'tradeoff':
        instance_response = requests.get(f"http://{config.REGISTRY_HOST}/services/{alias}/tradeoff")

    if instance_response is None or instance_response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for alias {alias}",
        )

    instance = instance_response.json()

    logger.debug(f"Serving with instance {instance['name']}")

    # redirect to provided instance
    url = f"http://{instance['name']}.weave.local{info['path']}"

    request = requests.Request(info['method'],
                               url,
                               data=info['body'],
                               headers=info['headers'],
                               params=info['query_params'])
    s = requests.Session()

    prepped = request.prepare()

    response = s.send(prepped)

    return Response(content=response.content, headers=response.headers, status_code=response.status_code)

