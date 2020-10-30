import os

from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_cloudformation as cloudformation,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    core,
)


class BastionHost(cloudformation.NestedStack):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(
            scope,
            id,
            **kwargs,
        )

        self.asg = autoscaling.AutoScalingGroup(
            self,
            "AutoScalingGroup",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ecs.EcsOptimizedAmi(),
            associate_public_ip_address=True,
            update_type=autoscaling.UpdateType.REPLACING_UPDATE,
            desired_capacity=1,
            vpc=scope.vpc,
            vpc_subnets={'subnet_type': ec2.SubnetType.PUBLIC},
        )

        self.cluster = ecs.Cluster(self, 'EcsCluster', vpc=scope.vpc)

        self.cluster.add_auto_scaling_group(self.asg)
        self.cluster.add_capacity(
            "DefaultAutoScalingGroup",
            instance_type=ec2.InstanceType("t2.micro"),
            max_capacity=2,
            key_name=os.environ.get("KEY_NAME"),
        )
