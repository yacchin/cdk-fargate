import os
from dotenv import load_dotenv

from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_ecs_patterns as ecs_patterns,
    core,
)

load_dotenv()

ROLE_ARN = os.environ["ROLE_ARN"]
ECR_REGISOTRY = os.environ["ECR_REGISOTRY"]


class CdkFargateStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(self, "CdkFargateVpc", max_azs=2)

        cluster = ecs.Cluster(self, "Ec2Cluster", vpc=vpc)

        role = iam.Role.from_role_arn(self, "Role", ROLE_ARN)
        image = ecs.ContainerImage.from_registry(ECR_REGISOTRY)
        task_definition = ecs.FargateTaskDefinition(
            scope=self, id="TaskDefinition", execution_role=role, task_role=role
        )
        port_mapping = ecs.PortMapping(container_port=80, host_port=80)
        container = task_definition.add_container(
            id="Container", image=image
        ).add_port_mappings(port_mapping)

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FargateService", cluster=cluster, task_definition=task_definition
        )

        core.CfnOutput(
            self,
            "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name,
        )
