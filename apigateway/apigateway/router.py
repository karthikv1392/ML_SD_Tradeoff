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
            "port": request.url.port,
            "scheme": request.url.scheme,
            "headers": request.headers,
            "query_params": request.query_params,
            "path_params": request.path_params,
            "host": request.client.host,
            "body": await request.body(),
            }

    # RANDOM RETRIEVE
    alias: str = utils.get_alias_by_path(info['path'])

    instance_response = requests.get(f"http://{config.REGISTRY_HOST}/services/{alias}")

    if instance_response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for alias {alias}",
        )

    instance = instance_response.json()

    logger.debug(f"Serving with instance {instance['name']}")

    # redirect to provided instance
    url = f"http://{instance['name']}.weave.local{info['path']}"
    logger.debug(url)

    request = requests.Request(info['method'],
                               url,
                               data=info['body'],
                               headers=info['headers'],
                               params=info['query_params'])
    s = requests.Session()

    prepped = request.prepare()

    response = s.send(prepped)

    logger.debug(response.content)

    # PING ALL INSTANCES
    # alias: str = utils.get_alias_by_path(info['path'])
    #
    # instances_response = requests.get(f"http://{config.REGISTRY_HOST}/services/{alias}/all")
    #
    # if instances_response.status_code == 404:
    #     raise HTTPException(
    #         status_code=404,
    #         detail=f"No service found for alias {alias}",
    #     )
    #
    # instances_name = instances_response.json()
    #
    # logger.debug(f"Found {len(instances_name)} instances.")
    #
    # response = None
    # for i_name in instances_name:  # redirect to all instances
    #
    #     url = f"http://{i_name}.weave.local{info['path']}"
    #     logger.debug(url)
    #
    #     request = requests.Request(info['method'],
    #                                url,
    #                                data=info['body'],
    #                                headers=info['headers'],
    #                                params=info['query_params'])
    #     s = requests.Session()
    #
    #     prepped = request.prepare()
    #
    #     response = s.send(prepped)
    #
    #     logger.debug(response.content)

    return Response(content=response.content, headers=response.headers, status_code=response.status_code)
