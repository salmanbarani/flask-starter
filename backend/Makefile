COMPOSE_RUN= docker compose -f local.yml

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build         	Build docker images"
	@echo "  up            	Run the docker containers"
	@echo "  logs      	   	To see logs"
	@echo "  down          	To stop containers and remove volumes"
	@echo "  test          	To run tests"
	@echo "  sh            	To start shell from the projct container"
	@echo "  flake8        	To check lintings"
	@echo "  black-check   	Using black to for linting check"
	@echo "  black-diff    	See linting differences before applying black"
	@echo "  black         	to apply black linting"
	@echo "  isort-check   	To check whether import sorts are correct"
	@echo "  isort-diff    	To see sorts differences"
	@echo "  isort         	To sort imports correctly"

build:
	$(COMPOSE_RUN) up --build -d --remove-orphans

up:
	$(COMPOSE_RUN) up -d

down:
	$(COMPOSE_RUN) down --remove-orphans

stop_postgres:
	$(COMPOSE_RUN) down postgres --remove-orphans

logs:
	$(COMPOSE_RUN) logs 

test : stop_postgres up
	$(COMPOSE_RUN) run --rm --no-deps --entrypoint=pytest api ./tests/unit ./tests/integration ./tests/e2e

sh:
	$(COMPOSE_RUN) run --rm -it api sh

flake8:
	$(COMPOSE_RUN) exec api flake8 .

black-check:
	$(COMPOSE_RUN) exec api black --check --exclude=migrations .

black-diff:
	$(COMPOSE_RUN) exec api black --diff --exclude=migrations .

black:
	$(COMPOSE_RUN) exec api black --exclude=migrations .

isort-check:
	$(COMPOSE_RUN) exec api isort . --check-only --skip env --skip migrations

isort-diff:
	$(COMPOSE_RUN) exec api isort . --diff --skip env --skip migrations

isort:
	$(COMPOSE_RUN) exec api isort . --skip env --skip migrations

all: down build up test