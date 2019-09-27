# -----------------------------------------------------------------------------
# BUILD
# -----------------------------------------------------------------------------
.PHONY: all
all: clean build

.PHONY: build
build:
	@docker-compose build
	@echo Build done.

.PHONY: use_local
use_local:
	@cp .env.local .env

.PHONY: use_docker
use_docker:
	@cp .env.docker .env

.PHONY: start
start:
	@docker-compose up -d
	@echo Start done.

.PHONY: stop
stop: stop_deps
	@docker-compose stop
	@echo Stop done.

.PHONY: clean
clean:
	@rm -rf .cache
	@rm -rf target
	@rm -f .version
	@find . -iname __pycache__ | xargs rm -rf
	@find . -iname "*.pyc" | xargs rm -f
	@find . -iname "mb*.log" | xargs rm -f
