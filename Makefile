ROOT_DIR := $(shell pwd)

DOCKER_BASE_IMAGE_TAG := distribrewed/core:x64
DOCKER_IMAGE_TAG := distribrewed/master:api-x64

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
	@$(MAKE) docker-stack-migrate

docker-stack-down:
	test ${DOCKER_STACK_DIR} != ""
	cd ${DOCKER_STACK_DIR} ;\
	docker-compose down

docker-stack-migrate:
	@sleep ${DOCKER_STACK_TIME_DELAY}
	@$(MAKE) django-manage ARG=migrate

django-manage: docker-build
	@docker run -it \
		--rm \
		--net=host \
		--env-file=${DOCKER_STACK_ENV_FILE} \
		-v ${ROOT_DIR}/distribrewed:/usr/project/distribrewed \
		-w /usr/project/distribrewed \
		${DOCKER_IMAGE_TAG} \
		python manage.py ${ARG}

django-chown:
	@set -xe ;\
	test $${USER} != "" ;\
	sudo chown $${USER}:$${USER} ${ROOT_DIR} -R
