ROOT_DIR := $(shell pwd)
IMAGE_TAG := distribrewed/master
BUILD_FLAGS ?= ''

docker-build:
	docker build ${BUILD_FLAGS} -t ${IMAGE_TAG} .