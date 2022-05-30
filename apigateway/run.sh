#!/bin/bash

NETWORK="ml_sd_tradeoff_monitoring"
IMAGE_NAME="ml_sd_tradeoff"
PORT="8000"
VERSION="0.0.1"
DNS="172.17.0.1"
DNS_SEARCH="weave.local"
ENV="REDIS_HOST=172.17.0.1 LB_STRATEGY=rr"
CONTAINER_NAME="ml_sd_tradeoff"

# CLEAN
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

if [ "$(docker images --filter dangling=true -q | wc -l)" -gt 0 ]; then
  docker rmi "$(docker images --filter dangling=true -q)" # remove dangling images
fi

# CHECK
if [ "$(redis-cli ping)" != "PONG" ]; then
  echo "Cannot reach Redis, exiting"
  exit 1
fi

if [ "$(redis-cli CONFIG SET protected-mode no)" != "OK" ]; then
  echo "Cannot set protected-mode no, exiting"
  exit 1
fi

# BUILD
docker build . -t $IMAGE_NAME:$VERSION

# RUN
docker run --name $CONTAINER_NAME --dns $DNS --dns-search $DNS_SEARCH --network $NETWORK -p $PORT:8000 --env $ENV $IMAGE_NAME:$VERSION



