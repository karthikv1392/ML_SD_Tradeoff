
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.orm import Session

from monitoring import db
from monitoring import services
from monitoring import utils

from loguru import logger
import json


router = APIRouter(
    tags=['monitoring'],
    prefix=''
)


@router.get('/data/{service_type}')
async def get_current_data(service_type: str, database: Session = Depends(db.get_db)):
    """Return updated data from the monitoring database"""

    data = services.get_current_data(database, service_type)

    data['calls'] = json.dumps(data['calls'].tolist())
    data['statuses'] = json.dumps(data['statuses'].tolist())
    return data


@router.get('/data/single/{instance}')
async def get_closest_entry(instance: str, timestamp: str, database: Session = Depends(db.get_db)):
    """Return the closest monitored data about an instance call"""
    timestamp = utils.read_timestamp(timestamp)
    call = services.get_closest_entry(database, instance, timestamp)
    return call

