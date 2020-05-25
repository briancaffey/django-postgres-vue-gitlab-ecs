import os

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_cloudformation as cloudformation,
    aws_elasticloadbalancingv2 as elbv2,
)


class FlowerServiceStack(cloudformation.NestedStack):
    def __init__(self, scope: core.Construct, id: str, **kwargs,) -> None:
        super().__init__(
            scope, id, **kwargs,
        )

        self.flower_task = ecs.FargateTaskDefinition(self, "FlowerTask")

        FLOWER_PASSWORD = os.environ.get("FLOWER_PASSWORD", "flowerpassword")
        REDIS_SERVICE_HOST = (
            scope.elasticache.elasticache.attr_redis_endpoint_address
        )
        CELERY_BROKER_URL = f"redis://{REDIS_SERVICE_HOST}:6379/0"
        self.flower_task.add_container(
            "BackendContainer",
            image=ecs.ContainerImage.from_registry("mher/flower"),
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="FlowerContainer",
                log_retention=logs.RetentionDays.ONE_DAY,
            ),
            command=[
                "--url_prefix=flower",
                f"--broker={CELERY_BROKER_URL}",
                f"--basic_auth=flower:{FLOWER_PASSWORD}",
            ],
        )

        scope.backend_assets_bucket.grant_read_write(
            self.backend_task.task_role
        )

        for secret in [scope.variables.django_secret_key, scope.rds.db_secret]:
            secret.grant_read(self.backend_task.task_role)

        port_mapping = ecs.PortMapping(
            container_port=5555, protocol=ecs.Protocol.TCP
        )
        self.flower_task.default_container.add_port_mappings(port_mapping)

        self.flower_service = ecs.FargateService(
            self,
            "FlowerService",
            task_definition=self.flower_task,
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
            targets=[self.flower_service],
            priority=1,
            path_patterns=["/flower/*"],
            health_check=elbv2.HealthCheck(healthy_http_codes="200-401",),
        )
