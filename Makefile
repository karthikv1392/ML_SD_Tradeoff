.POSIX:

# include config.mk

MAIN_COMPOSE = ./docker-compose/docker-compose.yml
TEST_COMPOSE = ./docker-compose/docker-compose.test.yml

.DEFAULT_GOAL := help

.SILENT: help
.PHONY: help # print this help text
help:
	@grep '^.PHONY: .* #' $(firstword $(MAKEFILE_LIST)) |\
		sed 's/\.PHONY: \(.*\) # \(.*\)/\1 # \2/' |\
		awk 'BEGIN {FS = "#"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.SILENT: weave_check
.PHONY: weave_check # weave-net and weave-scope check
weave_check:
	command -v weave > /dev/null || { \
		echo "ERROR: weave-net bin not found"; \
		sudo curl -L git.io/weave -o /usr/local/bin/weave; \
		sudo chmod a+x /usr/local/bin/weave; \
	}
	command -v scope > /dev/null || { \
		echo "ERROR: weave-scope bin not found"; \
		sudo curl -L git.io/scope -o /usr/local/bin/scope; \
		sudo chmod a+x /usr/local/bin/scope; \
	}

.SILENT: compose_check
.PHONY: compose_check # docker-compose yml files check
compose_check:
	if [ -z "$(MAIN_COMPOSE)" ]; then \
		echo "ERROR: MAIN_COMPOSE file not found"; \
		exit 1; \
	fi

.SILENT: docker_check
.PHONY: docker_check # docker and docker-compose check
docker_check:
	command -v docker > /dev/null || { \
		echo "ERROR: docker is not installed"; \
		exit 1; \
	}
	command -v docker-compose > /dev/null || { \
		echo "ERROR: docker-compose is not installed"; \
		exit 1; \
	}

.SILENT: redis_check
.PHONY: redis_check # docker and docker-compose check
redis_check:
	if [ -n "$(compgen -c | grep redis-server | sort -u)" ]; then \
		echo "ERROR: redis-server is not installed"; \
		exit 1; \
	fi


.SILENT: check
.PHONY: check # general check rule
check: weave_check compose_check docker_check redis_check

.SILENT: run
.PHONY: run
run: check
	echo "START: weave-net"
	weave launch
	echo "START: weave-scope"
	scope launch
	echo "BUILD: docker-compose build $(MAIN_COMPOSE)"
	docker-compose -f "$(MAIN_COMPOSE)" build -q
	echo "START: docker-compose up $(MAIN_COMPOSE)"
	docker-compose -f "$(MAIN_COMPOSE)" up -d

.SILENT: stop
.PHONY: stop
stop: check
	echo "STOP: docker-compose down $(MAIN_COMPOSE)"
	docker-compose -f "$(MAIN_COMPOSE)" down
	echo "CLEAN: docker system prune -f"
	docker system prune -f
	echo "STOP: weave-scope"
	scope stop
	echo "STOP: weave-net"
	weave stop
	echo "RESET: weave-net"
	weave reset --force
