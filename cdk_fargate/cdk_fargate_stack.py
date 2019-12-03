from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    core,
)


class CdkFargateStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        # Create VPC and Fargate Cluster
        # NOTE: Limit AZs to avoid reaching resource quotas
        vpc = ec2.Vpc(
            self, "CdkFargateVpc",
            max_azs=2
        )

        cluster = ecs.Cluster(
            self, 'Ec2Cluster',
            vpc=vpc
        )

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FargateService",
            cluster=cluster,
            task_image_options={
                'image': ecs.ContainerImage.from_registry("nginx")
            }
        )

        core.CfnOutput(
            self, "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name
        )
