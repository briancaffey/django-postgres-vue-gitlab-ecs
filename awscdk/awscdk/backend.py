import os

from aws_cdk import (
    core,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
)


class Backend(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        load_balancer,
        cluster: ecs.ICluster,
        domain_name: str,
        **kwargs,
    ) -> None:
        super().__init__(
            scope, id, **kwargs,
        )

        self.backend_task = ecs.FargateTaskDefinition(self, "BackendTask")

        environment_variables = {
            "DJANGO_SETTINGS_MODULE": "backend.settings.production",
            "DEBUG": "",
            "SECRET_KEY": "secret",
            "AWS_STORAGE_BUCKET_NAME": f"{domain_name.replace('.', '-')}-assets",  # noqa
        }

        self.backend_task.add_container(
            "nginx",
            image=ecs.AssetImage("../backend", file="scripts/prod/Dockerfile"),
            logging=ecs.LogDrivers.aws_logs(stream_prefix="Backend"),
            environment=environment_variables,
        )

        port_mapping = ecs.PortMapping(
            container_port=8000, protocol=ecs.Protocol.TCP
        )
        self.backend_task.default_container.add_port_mappings(port_mapping)

        self.backend_service = ecs.FargateService(
            self,
            "BackendService",
            task_definition=self.backend_task,
            assign_public_ip=True,
            cluster=cluster,
        )

        load_balancer.https_listener.add_targets(
            "BackendTarget",
            port=80,
            targets=[self.backend_service],
            priority=1,
            path_patterns=["*"],
        )
