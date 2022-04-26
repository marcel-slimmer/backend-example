.PHONY: run-quiz
.SILENT: ;
.DEFAULT_GOAL := help

GIT_SHA:=$(shell git rev-parse --short HEAD)
AWS_PROFILE:=default

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: ## Start pulumi environment
	pulumi login --local
	pulumi stack init ecs-baseline-dev
	pulumi config set aws:profile $(AWS_PROFILE)

deploy: provision exportconfig ## Deploy with -y

provision: ## Provision AWS Infra using Pulumi with -y
	pulumi up -y

exportconfig: ## Exports the kubernetes config
	gh secret set ECR_REPO_URL --body "$$(pulumi stack output --show-secrets ECR_REPO_URL)"
	gh secret set ECR_REPO_NAME --body "$$(pulumi stack output --show-secrets ECR_REPO_NAME)"
	gh secret set ECS_CLUSTER_NAME --body "$$(pulumi stack output --show-secrets ECS_CLUSTER_NAME)"
	gh secret set ECS_SERVICE_NAME --body "$$(pulumi stack output --show-secrets ECS_SERVICE_NAME)"
	gh secret set URL --body "$$(pulumi stack output --show-secrets URL)"

destroy: ## Destroy with -y
	pulumi destroy -y

rmstack: ## Remove stack with -y
	pulumi stack rm -y
