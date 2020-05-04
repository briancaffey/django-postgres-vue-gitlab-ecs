from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    core,
)


class Ecs(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        vpc: ec2.IVpc,
        domain_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.cluster = ecs.Cluster(
            self,
            "EcsCluster",
            vpc=vpc,
            cluster_name=f"{domain_name.replace('.', '-')}-cluster",
        )
