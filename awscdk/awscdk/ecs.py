from aws_cdk import aws_ecs as ecs, aws_ec2 as ec2, aws_autoscaling as autoscaling, core


class Ecs(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        vpc: ec2.IVpc,
        # assets: core.Construct,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc)

        # self.asg = autoscaling.AutoScalingGroup(
        #     self,
        #     "AutoScalingGroup",
        #     instance_type=ec2.InstanceType("t2.micro"),
        #     machine_image=ecs.EcsOptimizedAmi(),
        #     update_type=autoscaling.UpdateType.REPLACING_UPDATE,
        #     desired_capacity=1,
        #     vpc=vpc,
        #     vpc_subnets={"subnet_type": ec2.SubnetType.PUBLIC},
        # )

        # assets.assets_bucket.grant_read_write(self.asg)

        # self.cluster.add_auto_scaling_group(self.asg)
