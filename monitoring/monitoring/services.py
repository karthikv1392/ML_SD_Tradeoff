import os

from loguru import logger
from datetime import datetime, timedelta

from sqlalchemy import and_

from monitoring.tables import ServiceStatus, ServiceCall, Workload
import monitoring.db as db
import pandas as pd

database = next(db.get_db())

ts_format = '%Y-%m-%d %H:%M:%S.%f'


def store_service_status(service_status: ServiceStatus):
    database.add(service_status)
    database.commit()
    database.refresh(service_status)

    # logger.debug(f"Successfully added Service Status with id: {service_status.id}")


def store_service_call(service_call: ServiceCall):
    database.add(service_call)
    database.commit()

    database.refresh(service_call)

    # logger.debug(f"Successfully added Service Call with id: {service_call.id}")


def store_workload(ts_init, ts_end, days_count, day_duration, label):
    ts_init = datetime.strptime(ts_init, ts_format)
    ts_end = datetime.strptime(ts_end, ts_format)

    # subtract two hours for dmon timezone error
    ts_init = ts_init - timedelta(hours=2)
    ts_end = ts_end - timedelta(hours=2)

    workload: Workload = Workload(ts_init=ts_init, ts_end=ts_end, days_count=days_count, day_duration=day_duration,
                                  label=label)
    database.add(workload)
    database.commit()

    database.refresh(workload)

    logger.debug(f"Successfully added Workload with id: {workload.id}")


def generate_rt_csv_by_workload_id(wl_id: int, folder: str):
    # Check whether the specified path exists or not
    is_exist = os.path.exists(folder)

    if not is_exist:
        # Create a new directory because it does not exist
        os.makedirs(folder)
        logger.debug(f"Folder {folder} created")

    wl = database.query(Workload).get(wl_id)

    if wl is None:
        logger.error(f"No workload found for id {wl_id}")
        return

    logger.debug(wl.ts_init)
    logger.debug(wl.ts_end)

    calls = database.query(ServiceCall).filter(and_(
        ServiceCall.timestamp >= wl.ts_init), (
        ServiceCall.timestamp <= wl.ts_end)
    )

    # using the query object to create the pandas dataframe
    calls_df = pd.read_sql(calls.statement, calls.session.bind)
    calls_df.to_csv(f"{folder}/workload_{wl_id}.csv")
    logger.debug(len(calls_df))


def generate_cpu_csv_by_workload_id(wl_id: int, folder: str):
    # Check whether the specified path exists or not
    is_exist = os.path.exists(folder)

    if not is_exist:
        # Create a new directory because it does not exist
        os.makedirs(folder)
        logger.debug(f"Folder {folder} created")

    wl = database.query(Workload).get(wl_id)

    if wl is None:
        logger.error(f"No workload found for id {wl_id}")
        return

    logger.debug(wl.ts_init)
    logger.debug(wl.ts_end)

    calls = database.query(ServiceStatus).filter(and_(
        ServiceStatus.timestamp >= wl.ts_init), (
        ServiceStatus.timestamp <= wl.ts_end)
    )

    # using the query object to create the pandas dataframe
    calls_df = pd.read_sql(calls.statement, calls.session.bind)
    calls_df.to_csv(f"{folder}/workload_{wl_id}.csv")
    logger.debug(len(calls_df))

