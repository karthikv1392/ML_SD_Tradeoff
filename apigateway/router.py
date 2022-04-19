from loguru import logger
from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse

from .services import MonitoringService
from .app_services import get_main_service_registry
from .utils import get_path_alias
from apigateway.registry.models import ServiceInspector, ServiceInstance

router = APIRouter(
    tags=['apigateway'],
    prefix=''
)


@router.api_route('/{full_path:path}', methods=["GET", "POST", "PUT", "DELETE"])
async def get_interceptor(request: Request, full_path: str, monitoring_service: MonitoringService = Depends(get_main_service_registry)):

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

    service_registry = monitoring_service.get_main_registry().get_registry()

    # retrieve service requested by his alias, i.e. first part of path
    service_alias = get_path_alias(info["path"])
    logger.debug(f"Service alias detected: {service_alias}")
    inspector: ServiceInspector = service_registry.retrieve_inspector_by_alias(service_alias)
    logger.debug(f"Inspector found: {inspector.name}")

    # ask registry to provide a valid service instance
    instance: ServiceInstance = inspector.get_random_instance()
    logger.debug(f"Serving with instance {instance.name}")

    # redirect to provided instance
    return RedirectResponse(f"http://localhost:{instance.get_default_port()}{info['path']}")
