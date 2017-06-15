ROOT_DIR := $(shell pwd)
IMAGE_TAG := distribrewed/master

docker-build:
	docker build -t ${IMAGE_TAG} .