from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_ecs_patterns as ecs_patterns,
    aws_logs as logs,
    aws_cloudformation as cloudformation,
    aws_cloudwatch as cw,
    aws_applicationautoscaling as aas,
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
            desired_count=0,
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

        self.default_celery_queue_cw_metric = cw.Metric(
            namespace=scope.full_app_name, metric_name="default"
        )

        self.celery_default_queue_asg = self.celery_default_worker_service.auto_scale_task_count(
            min_capacity=0, max_capacity=2
        )

        self.celery_default_queue_asg.scale_on_metric(
            "CeleryDefaultQueueAutoscaling",
            metric=self.default_celery_queue_cw_metric,
            scaling_steps=[
                aas.ScalingInterval(change=-1, lower=0),
                aas.ScalingInterval(change=1, lower=1),
            ],
            adjustment_type=aas.AdjustmentType.CHANGE_IN_CAPACITY,
        )
