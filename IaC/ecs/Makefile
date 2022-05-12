.PHONY: help init deploy provision destroy rmstack
.SILENT: ;
.DEFAULT_GOAL := help

GIT_SHA:=$(shell git rev-parse --short HEAD)
AWS_PROFILE:=default
PULUMI_STATE_URL:=s3://pulumi-state-manager
PULUMI_STACK_NAME:=ecs-baseline-dev

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: ## Start pulumi environment
	test -s $${HOME}/.pulumi/passphrase.txt || read -s -p "Enter Password for pulumi: " my_password && echo $${my_password} > $${HOME}/.pulumi/passphrase.txt
	docker-compose run --name pulumi-local --entrypoint bash --rm pulumi -c "pulumi login $(PULUMI_STATE_URL) && pulumi stack init $(PULUMI_STACK_NAME)"

addpylib: ## Rebuild after add lib in requirements.txt
	docker-compose kill
	docker-compose build --no-cache pulumi

deploy: provision ## Deploy with -y

provision: ## Provision AWS Infra using Pulumi with -y
	docker-compose run --name pulumi-local --entrypoint bash --rm pulumi -c "pulumi login $(PULUMI_STATE_URL) && pulumi stack select $(PULUMI_STACK_NAME) && pulumi up -y"

destroy: ## Destroy with -y
	docker-compose run --name pulumi-local --entrypoint bash --rm pulumi -c "pulumi login $(PULUMI_STATE_URL) && pulumi stack select $(PULUMI_STACK_NAME) && pulumi destroy -y"

rmstack: ## Remove stack with -y
	docker-compose run --name pulumi-local --entrypoint bash --rm pulumi -c "pulumi login $(PULUMI_STATE_URL) && pulumi stack select $(PULUMI_STACK_NAME) && pulumi stack rm -y"

check: ## Remove stack with -y
	docker-compose run --name pulumi-local --entrypoint bash --rm pulumi -c "pulumi version"
