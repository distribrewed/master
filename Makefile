ROOT_DIR := $(shell pwd)

DOCKER_BASE_IMAGE_TAG := distribrewed/core:x64
DOCKER_IMAGE_TAG := distribrewed/master:api-x64

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
	./travis_scripts/build_x64.sh

docker-stack-up:
	test ${DOCKER_STACK_DIR} != ""
	cd ${DOCKER_STACK_DIR} ;\
	docker-compose up -d
	cd ${ROOT_DIR}
	@$(MAKE) docker-stack-dev-createsuperuser

docker-stack-down:
	test ${DOCKER_STACK_DIR} != ""
	cd ${DOCKER_STACK_DIR} ;\
	docker-compose down

docker-stack-migrate:
	@sleep ${DOCKER_STACK_TIME_DELAY}
	@$(MAKE) django-manage ARG=migrate

docker-stack-dev-createsuperuser: docker-stack-migrate
	@$(MAKE) django-manage ARG="createsuperuser --username admin --email admin@admin.admin"

docker-pull-workers:
	docker pull distribrewed/workers:x64

docker-run-worker: docker-pull-workers
	docker run -it $(DOCKER_STACK_RABBITMQ_LINK) -e WORKER_PLUGIN_CLASS=TemperatureWorker distribrewed/workers:x64

django-manage: docker-build
	@docker run -it \
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