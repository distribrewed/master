ROOT_DIR := $(shell pwd)

DOCKER_BASE_IMAGE_TAG := distribrewed/core:x64
DOCKER_IMAGE_TAG := distribrewed/master

DOCKER_STACK_DB_CONTAINER_NAME ?= distribrewedstack_postgres_1
DOCKER_STACK_DB_LINK ?= --link=${DOCKER_STACK_DB_CONTAINER_NAME}:postgres

DOCKER_STACK_RABBITMQ_CONTAINER_NAME ?= distribrewedstack_rabbitmq_1
DOCKER_STACK_RABBITMQ_LINK ?= --link=${DOCKER_STACK_RABBITMQ_CONTAINER_NAME}:rabbitmq

DOCKER_STACK_TIME_DELAY := 5
DOCKER_STACK_DIR := ${ROOT_DIR}/distribrewed_stack
DOCKER_STACK_ENV_FILE ?= ${DOCKER_STACK_DIR}/.env

docker-pull-base:
	docker pull ${DOCKER_BASE_IMAGE_TAG}

docker-build: docker-pull-base
	docker build ${BUILD_FLAGS} -t ${DOCKER_IMAGE_TAG} .

docker-stack-up:
	test ${DOCKER_STACK_DIR} != ""
	cd ${DOCKER_STACK_DIR} ;\
	docker-compose up -d
	cd ${ROOT_DIR}
	@$(MAKE) docker-stack-migrate

docker-stack-down:
	test ${DOCKER_STACK_DIR} != ""
	cd ${DOCKER_STACK_DIR} ;\
	docker-compose down

docker-stack-migrate:
	@sleep ${DOCKER_STACK_TIME_DELAY}
	@$(MAKE) django-manage ARG=migrate


django-manage: docker-build
	docker run -it \
		--rm \
		${DOCKER_STACK_DB_LINK} \
		--env-file=${DOCKER_STACK_ENV_FILE} \
		-v ${ROOT_DIR}/distribrewed:/opt/project/distribrewed \
		-w /opt/project/distribrewed \
		${DOCKER_IMAGE_TAG} \
		python manage.py ${ARG}

django-chown:
	@set -xe ;\
	test $${USER} != "" ;\
	sudo chown $${USER}:$${USER} ${ROOT_DIR} -R