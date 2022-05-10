from pulumi import Config, Output
from pulumi_aws import ec2, iam, ssm
import json

import vpc

# Create a SecurityGroup that permits HTTP ingress and unrestricted egress.
group = ec2.SecurityGroup('web-secgrp',
                          vpc_id=vpc.default_vpc.id,
                          description='Enable HTTP access',
                          ingress=[ec2.SecurityGroupIngressArgs(
                              protocol='tcp',
                              from_port=80,
                              to_port=80,
                              cidr_blocks=['0.0.0.0/0'],
                          )],
                          egress=[ec2.SecurityGroupEgressArgs(
                              protocol='-1',
                              from_port=0,
                              to_port=0,
                              cidr_blocks=['0.0.0.0/0'],
                          )],
                          )

# Create an IAM role that can be used by our service's task.
role = iam.Role('task-exec-role',
                assume_role_policy=json.dumps({
                    'Version': '2008-10-17',
                    'Statement': [{
                        'Sid': '',
                        'Effect': 'Allow',
                        'Principal': {
                            'Service': 'ecs-tasks.amazonaws.com'
                        },
                        'Action': 'sts:AssumeRole',
                    }]
                }),
                )

rpa = iam.RolePolicyAttachment('task-exec-policy',
                               role=role.name,
                               policy_arn='arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy',
                               )

# Set permission to access SSM new relic parameter
nr_config = Config('new_relic')
nr_license_key = nr_config.require('license_key')

ecs_ssm_parameter = ssm.Parameter("/newrelic-infra/ecs/license-key",
                                  description="New Relic license key for ECS monitoring",
                                  type="SecureString",
                                  value=nr_license_key)

ecs_ssm_parameter_role_policy = iam.RolePolicy('NewRelicSSMLicenseKeyReadAccess',
                                               role=role.id,
                                               policy=Output.all(
                                                   ecs_ssm_parameter.arn).apply(lambda args: json.dumps({
                                                       "Version": "2012-10-17",
                                                       "Statement": [{
                                                           "Effect": "Allow",
                                                           "Action": [
                                                               "ssm:GetParameters"
                                                           ],
                                                           "Resource": args[0]
                                                       }]
                                                   }))
                                               )
