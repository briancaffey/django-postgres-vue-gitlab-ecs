from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_cloudformation as cloudformation,
    aws_elasticloadbalancingv2 as elbv2,
)


class BackendServiceStack(cloudformation.NestedStack):
    def __init__(self, scope: core.Construct, id: str, **kwargs,) -> None:
        super().__init__(
            scope, id, **kwargs,
        )

        self.backend_task = ecs.FargateTaskDefinition(self, "BackendTask")

        self.backend_task.add_container(
            "BackendContainer",
            image=scope.image,
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="BackendContainer",
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
            environment=scope.variables.regular_variables,
            secrets=scope.variables.secret_variables,
            command=["/start_prod.sh"],
        )

        scope.backend_assets_bucket.grant_read_write(
            self.backend_task.task_role
        )

        for secret in [scope.variables.django_secret_key, scope.rds.db_secret]:
            secret.grant_read(self.backend_task.task_role)

        port_mapping = ecs.PortMapping(
            container_port=8000, protocol=ecs.Protocol.TCP
        )
        self.backend_task.default_container.add_port_mappings(port_mapping)

        self.backend_service = ecs.FargateService(
            self,
            "BackendService",
            task_definition=self.backend_task,
            assign_public_ip=True,
            cluster=scope.ecs.cluster,
            security_group=ec2.SecurityGroup.from_security_group_id(
                self,
                "BackendServiceSecurityGroup",
                security_group_id=scope.vpc.vpc_default_security_group,
            ),
        )

        scope.https_listener.add_targets(
            "BackendTarget",
            port=80,
            targets=[self.backend_service],
            priority=1,
            path_patterns=["*"],
            health_check=elbv2.HealthCheck(
                healthy_http_codes="200-299", path="/api/hello-world",
            ),
        )
