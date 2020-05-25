from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_cloudformation as cloudformation,
)


class CeleryDefaultServiceStack(cloudformation.NestedStack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(
            scope, id, **kwargs,
        )

        self.celery_default_worker_task = ecs.FargateTaskDefinition(
            self, "DefaultCeleryWorkerFargateTask"
        )

        self.celery_default_worker_task.add_container(
            "DefaultCeleryWorkerContaienr",
            image=scope.image,
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="CeleryDefaultWorkerContainer",
                log_retention=logs.RetentionDays.ONE_WEEK,
            ),
            environment=scope.variables.regular_variables,
            secrets=scope.variables.secret_variables,
            command=[
                'celery',
                'worker',
                '-A',
                'backend.celery_app:app',
                '-l',
                'info',
                '-Q',
                'default',
                '-n',
                'worker-default@%h',
            ],
        )

        self.celery_default_worker_service = ecs.FargateService(
            self,
            "DefaultCeleryWorkerService",
            task_definition=self.celery_default_worker_task,
            assign_public_ip=True,
            cluster=scope.ecs.cluster,
            security_group=ec2.SecurityGroup.from_security_group_id(
                self,
                "CeleryDefaultWorkerSG",
                security_group_id=scope.vpc.vpc_default_security_group,
            ),
        )

        scope.backend_assets_bucket.grant_read_write(
            self.celery_default_worker_service.task_definition.task_role
        )

        for secret in [scope.variables.django_secret_key, scope.rds.db_secret]:
            secret.grant_read(
                self.celery_default_worker_service.task_definition.task_role
            )
