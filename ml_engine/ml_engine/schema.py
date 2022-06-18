import datetime
from typing import List

from pydantic import BaseModel


class RtEntry(BaseModel):
    id: int
    timestamp: datetime
    time_delta: float
    service_instance: str
    service_type: str


class RtPayload(BaseModel):
    payload: List[RtEntry]
