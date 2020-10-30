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
            security_group=ec2.SecurityGroup.from_security_group_id(
                self,
                "DefaultSecurityGroupId",
                scope.vpc.vpc_default_security_group,
            ),
            associate_public_ip_address=True,
            update_type=autoscaling.UpdateType.REPLACING_UPDATE,
            desired_capacity=1,
            vpc=scope.vpc,
            key_name=os.environ.get("KEY_NAME"),
            vpc_subnets={'subnet_type': ec2.SubnetType.PUBLIC},
        )

        self.cluster = scope.cluster

        self.cluster.add_auto_scaling_group(self.asg)

        self.bastion_host_task = ecs.Ec2TaskDefinition(self, "BastionHostTask")

        self.bastion_host_task.add_container(
            image=scope.image,
            command=["/start_prod.sh"],
            environment=scope.variables.regular_variables,
            secrets=scope.variables.secret_variables,
        )

        self.bastion_host_service = ecs.Ec2Service(
            self,
            "BastionHostService",
            task_definition=self.bastion_host_task,
            cluster=self.cluster,
        )
