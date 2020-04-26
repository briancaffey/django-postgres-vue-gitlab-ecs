from aws_cdk import core

from aws_cdk import (
    aws_ec2 as ec2
)


class Vpc(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "Vpc",
            max_azs=2,
            cidr="10.0.0.0/16",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.ISOLATED,
                    name="Isolated",
                    cidr_mask=24
                )
            ]
        )
