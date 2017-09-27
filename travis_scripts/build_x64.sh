#!/bin/bash

set -e

docker build -t distribrewed/master:queue-x64 -f Dockerfile .
docker build -t distribrewed/master:api-x64 -f Dockerfile.api .

if [[ ${TRAVIS} == "true" ]]; then
    docker login -u="$DOCKER_USER" -p="$DOCKER_PASS"
    docker push distribrewed/master:queue-x64
    docker push distribrewed/master:api-x64
fi