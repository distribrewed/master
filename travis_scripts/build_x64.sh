#!/bin/sh

set -e

docker build -t distribrewed/master:x64 -f Dockerfile .
docker login -u="$DOCKER_USER" -p="$DOCKER_PASS"
docker push distribrewed/master:x64