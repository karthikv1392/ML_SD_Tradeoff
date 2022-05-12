from loguru import logger
from datetime import datetime

from monitoring.tables import ServiceStatus, ServiceCall, Workload
import monitoring.db as db

database = next(db.get_db())

ts_format = '%Y-%m-%d %H:%M:%S.%f'

def store_service_status(service_status: ServiceStatus):
    database.add(service_status)
    database.commit()
    database.refresh(service_status)

    logger.debug(f"Successfully added Service Status with id: {service_status.id}")


def store_service_call(service_call: ServiceCall):
    database.add(service_call)
    database.commit()

    database.refresh(service_call)

    logger.debug(f"Successfully added Service Call with id: {service_call.id}")


def store_workload(ts_init, ts_end, days_count, day_duration):
    ts_init = datetime.strptime(ts_init, ts_format)
    ts_end = datetime.strptime(ts_end, ts_format)

    workload: Workload = Workload(ts_init=ts_init, ts_end=ts_end, days_count=days_count, day_duration=day_duration)
    database.add(workload)
    database.commit()

    database.refresh(workload)

    logger.debug(f"Successfully added Workload with id: {workload.id}")

