import os


APP_ENV = os.getenv('APP_ENV', 'dev')
DMON_REDIS_HOST = os.getenv('DMON_REDIS_HOST', '127.0.0.1')
DMON_REDIS_PORT = os.getenv('DMON_REDIS_PORT', '6379')
DMON_REDIS_DB = os.getenv('DMON_REDIS_DB', '1')

DMON_NETWORK_TOPIC = os.getenv('DMON_NETWORK_TOPIC', 'dmon_network_out')
DMON_STRUCTURE_TOPIC = os.getenv('DMON_STRUCTURE_TOPIC', 'dmon_structure_out')
DMON_MERGED_TOPIC = os.getenv('DMON_MERGED_TOPIC', 'dmon_merged_out')

DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '65rgvc')
DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'monitoring')
TEST_DATABASE_NAME = os.getenv('DATABASE_NAME', 'test_sm')
