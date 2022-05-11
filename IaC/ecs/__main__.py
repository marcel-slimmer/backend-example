from pulumi import export, ResourceOptions, Output, Config
from pulumi_aws import ecs, cloudwatch, get_region
import json

import vpc
import iam
import alb
import ecr

current_region = get_region()

# Create an ECS cluster to run a container-based service.
cluster = ecs.Cluster('cluster',
                      tags={
                          'Name': 'app-ecs-cluster',
                      })

ecs_log_group = cloudwatch.LogGroup("ecs-log-group",
                                    retention_in_days=1,
                                    name="ecs-log-group"
                                    )

# Spin up a load balanced service running our container image.
task_definition = ecs.TaskDefinition('app-task',
                                     family='fargate-task-definition',
                                     cpu='256',
                                     memory='512',
                                     network_mode='awsvpc',
                                     requires_compatibilities=['FARGATE'],
                                     execution_role_arn=iam.role.arn,
                                     container_definitions=Output.all(
                                         ecr.api_image.image_name).apply(lambda args: json.dumps([
                                             {
                                                 'name': 'backend-app',
                                                 'image': args[0],
                                                 'portMappings': [{
                                                     'containerPort': 80,
                                                     'hostPort': 80,
                                                     'protocol': 'tcp'
                                                 }],
                                                 "logConfiguration": {
                                                     "logDriver": "awslogs",
                                                     "options": {
                                                         "awslogs-group": "ecs-log-group",
                                                         "awslogs-region": current_region.name,
                                                         "awslogs-stream-prefix": "app-task",
                                                     },
                                                 },
                                             },
                                         ])
                                     ))

service = ecs.Service('app-svc',
                      name='backend',
                      cluster=cluster.arn,
                      desired_count=1,
                      launch_type='FARGATE',
                      task_definition=task_definition.arn,
                      network_configuration=ecs.ServiceNetworkConfigurationArgs(
                          assign_public_ip=True,
                          subnets=vpc.default_vpc_subnets.ids,
                          security_groups=[iam.group.id],
                      ),
                      load_balancers=[ecs.ServiceLoadBalancerArgs(
                          target_group_arn=alb.atg.arn,
                          container_name='backend-app',
                          container_port=80,
                      )],
                      opts=ResourceOptions(depends_on=[alb.wl]),
                      )

export('URL', alb.alb.dns_name)
export('ECS_SERVICE_NAME', service.name)
export('ECS_CLUSTER_NAME', cluster.name)
export('ECR_REPO_NAME', ecr.ecr_repo.name)
export('ECR_REPO_URL', ecr.ecr_repo.repository_url)
