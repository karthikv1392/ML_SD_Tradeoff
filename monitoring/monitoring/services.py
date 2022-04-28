from loguru import logger

from monitoring.tables import ServiceStatus, ServiceCall
import monitoring.db as db

database = next(db.get_db())


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

