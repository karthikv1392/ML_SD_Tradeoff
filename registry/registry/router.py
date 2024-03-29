from typing import Dict

from loguru import logger
from fastapi import APIRouter, Request, Response, Depends, HTTPException

from registry.app_services import get_registry_provider
from registry.models import ServiceRegistry, ServiceInspector, ServiceInstance
from registry.services import RegistryProviderService
from registry import services
from registry import config

router = APIRouter(
    tags=['registry'],
    prefix=''
)


@router.get('/registry')
async def get_registry(registry_provider: RegistryProviderService = Depends(get_registry_provider)):
    """Return the main registry"""

    registry_provider = registry_provider.get_registry_provider()
    service_registry: ServiceRegistry = registry_provider.get_registry_instance()

    return service_registry


@router.get('/services/{alias}')
async def get_random_instance(alias: str, registry_provider: RegistryProviderService = Depends(get_registry_provider)):
    """Return a random service instance by one of its service aliases"""

    registry_provider = registry_provider.get_registry_provider()
    service_registry: ServiceRegistry = registry_provider.get_registry_instance()

    inspector: ServiceInspector = service_registry.retrieve_inspector_by_alias(alias)

    if inspector is not None:
        instance: ServiceInstance = inspector.get_random_instance()

        return {"type": inspector.name, "name": instance.name}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for alias {alias}",
        )


@router.get('/services/{alias}/rr')
async def get_rr_instance(alias: str, registry_provider: RegistryProviderService = Depends(get_registry_provider)):
    """Return the next service instance by one of its service aliases with the round robin balancing"""

    registry_provider = registry_provider.get_registry_provider()
    service_registry: ServiceRegistry = registry_provider.get_registry_instance()

    inspector: ServiceInspector = service_registry.retrieve_inspector_by_alias(alias)

    if inspector is not None:
        instance: ServiceInstance = inspector.get_round_robin_instance()

        return {"type": inspector.name, "name": instance.name}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for alias {alias}",
        )


@router.get('/services/{alias}/tradeoff')
async def get_tradeoff_instance(alias: str, registry_provider: RegistryProviderService = Depends(get_registry_provider)):
    """Return the next service instance by one of its service aliases with the tradeoff balancing"""

    registry_provider = registry_provider.get_registry_provider()
    service_registry: ServiceRegistry = registry_provider.get_registry_instance()

    inspector: ServiceInspector = service_registry.retrieve_inspector_by_alias(alias)

    logger.debug(f"ML engine endpoint: {config.ML_ENGINE_HOST}")
    if inspector is None:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for alias {alias}",
        )

    instance = services.get_tradeoff_instance(inspector.name)
    return {"type": inspector.name, "name": instance}


@router.get('/services/by-ip/{ip}')
async def get_instance_by_ip(ip: str, registry_provider: RegistryProviderService = Depends(get_registry_provider)):
    """Return the service instance associated with a given ip, if found"""
    registry_provider = registry_provider.get_registry_provider()
    service_registry: ServiceRegistry = registry_provider.get_registry_instance()
    logger.debug(f"ip: {ip}")
    retrieved_instance = service_registry.search_by_ip_address(ip)

    if retrieved_instance is None:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for ip {ip}",
        )
    return retrieved_instance


@router.get('/services/by-name/{instance_name}')
async def get_instance_by_name(instance_name: str, registry_provider: RegistryProviderService = Depends(get_registry_provider)):
    """Return the service instane associated with the given name, if found"""
    registry_provider = registry_provider.get_registry_provider()
    service_registry: ServiceRegistry = registry_provider.get_registry_instance()

    instance = service_registry.search_by_name(instance_name)

    if instance is None:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for name {instance_name}",
        )
    return instance


@router.get('/services/{alias}/all')
async def get_all_instances_by_alias(alias: str, registry_provider: RegistryProviderService = Depends(get_registry_provider)):

    registry_provider = registry_provider.get_registry_provider()
    service_registry: ServiceRegistry = registry_provider.get_registry_instance()

    inspector: ServiceInspector = service_registry.retrieve_inspector_by_alias(alias)

    if inspector is not None:
        instances_name = inspector.get_all_instances()

        return instances_name
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for alias {alias}",
        )


@router.get('/services/{type}/instances')
async def get_all_instances_by_alias(type: str,
                                        registry_provider: RegistryProviderService = Depends(get_registry_provider)):

    registry_provider = registry_provider.get_registry_provider()
    service_registry: ServiceRegistry = registry_provider.get_registry_instance()

    inspector: ServiceInspector = service_registry.retrieve_inspector_by_type(type)

    if inspector is not None:
        instances_name = inspector.get_all_instances()

        return instances_name
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No service found for type {type}",
        )

