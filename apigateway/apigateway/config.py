import os


APP_ENV = os.getenv('APP_ENV', 'dev')

REGISTRY_HOST = os.getenv('REGISTRY_HOST', '172.17.0.1:8001')

LB_STRATEGY = os.getenv('LB_STRATEGY', 'rr')  # rr | random | tradeoff
