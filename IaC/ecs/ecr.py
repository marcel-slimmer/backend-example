import base64

from pulumi import ResourceOptions
from pulumi_aws import ecr
import pulumi_docker as docker


# Get registry info (creds and endpoint).
def get_registry_info(rid):
    creds = ecr.get_credentials(registry_id=rid)
    decoded = base64.b64decode(creds.authorization_token).decode()
    parts = decoded.split(':')
    if len(parts) != 2:
        raise Exception("Invalid credentials")
    return docker.ImageRegistry(creds.proxy_endpoint, parts[0], parts[1])


ecr_repo = ecr.Repository("baseline-example",
                          image_scanning_configuration=ecr.RepositoryImageScanningConfigurationArgs(
                              scan_on_push=True,
                          ),
                          image_tag_mutability="MUTABLE")

ecr_lc_policy = ecr.LifecyclePolicy("policy-baseline-example",
                                    repository=ecr_repo.name,
                                    policy="""{
                                        "rules": [
                                            {
                                                "rulePriority": 1,
                                                "description": "Expire images older than 1 days",
                                                "selection": {
                                                    "tagStatus": "untagged",
                                                    "countType": "sinceImagePushed",
                                                    "countUnit": "days",
                                                    "countNumber": 1
                                                },
                                                "action": {
                                                    "type": "expire"
                                                }
                                            }
                                        ]
                                    }"""
                                    )

image_name = ecr_repo.repository_url
registry_info = ecr_repo.registry_id.apply(get_registry_info)


api_image = docker.Image("api_docker_image",
                         image_name=image_name,
                         build="../../",
                         skip_push=False,
                         registry=registry_info,
                         opts=ResourceOptions(depends_on=[ecr_repo]),
                         )
