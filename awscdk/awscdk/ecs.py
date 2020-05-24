from aws_cdk import (
    aws_ecs as ecs,
    aws_cloudformation as cloudformation,
    aws_ec2 as ec2,
    core,
)


class EcsStack(cloudformation.NestedStack):
    def __init__(self, scope: core.Construct, id: str, **kwargs,) -> None:
        super().__init__(scope, id, **kwargs)

        self.cluster = ecs.Cluster(
            self,
            "EcsCluster",
            vpc=scope.vpc,
            cluster_name=f"{scope.full_app_name}-cluster",
        )
