from loguru import logger
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from edge_router.utils import get_path_alias
from service_registry.models import ServiceRegistry, ServiceInspector, ServiceInstance

router = APIRouter(
    tags=['edge_router'],
    prefix=''
)

registry: ServiceRegistry = ServiceRegistry()


@router.api_route('/{full_path:path}', methods=["GET", "POST", "PUT", "DELETE"])
async def get_interceptor(request: Request, full_path: str):
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
    logger.debug(info)

    # retrieve service requested by his alias, i.e. first part of path
    service_alias = get_path_alias(info["path"])
    logger.debug(f"Service alias detected: {service_alias}")
    inspector: ServiceInspector = registry.retrieve_inspector_by_alias(service_alias)
    logger.debug(f"Inspector found: {inspector.name}")

    # ask registry to provide a valid service instance
    instance: ServiceInstance = inspector.get_random_instance()
    logger.debug(f"Serving with instance {instance.host}:{instance.port}")

    # redirect to provided instance
    return RedirectResponse(f"http://{instance.host}:{instance.port}{info['path']}")
