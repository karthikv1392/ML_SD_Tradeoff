import os


APP_ENV = os.getenv('APP_ENV', 'dev')
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_DB = os.getenv('REDIS_DB', '1')

DMON_NETWORK_TOPIC = os.getenv('DMON_NETWORK_TOPIC', 'dmon_network_out')
DMON_STRUCTURE_TOPIC = os.getenv('DMON_STRUCTURE_TOPIC', 'dmon_structure_out')
DMON_MERGED_TOPIC = os.getenv('DMON_MERGED_TOPIC', 'dmon_merged_out')

DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'ml_sd_tradeoff')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '65rgvc')
DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'monitoring')
TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME', 'test_sm')

REGISTRY_HOST = os.getenv('REGISTRY_HOST', '172.17.0.1:8001')
