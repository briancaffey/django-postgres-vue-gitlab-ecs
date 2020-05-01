import os

from aws_cdk import core, aws_ec2 as ec2, aws_rds as rds, aws_ssm as ssm


class Rds(core.Construct):
    def __init__(self, scope: core.Construct, id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.rds = rds.DatabaseInstance(
            self,
            "RdsInstance",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            master_username="postgres",
            instance_class=ec2.InstanceType(instance_type_identifier="t2.small"),
            vpc=vpc,
            vpc_placement=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
        )
