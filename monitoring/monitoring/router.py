from typing import Dict

from loguru import logger
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.orm import Session

from monitoring import db
from monitoring import services
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
