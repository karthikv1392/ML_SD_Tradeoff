from redis import Redis
from loguru import logger

from apigateway.config import REDIS_HOST, REDIS_PORT, REDIS_DB


def init_redis_client():
    """Initiliaze a redis client with the info present in the config file"""
    redis_client = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB
    )

    redis_client.ping()
    logger.info("Successfully connected to redis")
    return redis_client


def get_subscriber(redis_client: Redis, topic: str):
    """Creates a new subscriber to a given redis client and topic"""
    sub = redis_client.pubsub()
    sub.subscribe(topic)
    return sub
