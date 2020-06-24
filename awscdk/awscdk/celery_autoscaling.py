from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_events as events,
    aws_lambda,
    aws_events_targets as events_targets,
    aws_logs as logs,
    aws_cloudformation as cloudformation,
)


class CeleryAutoscalingStack(cloudformation.NestedStack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(
            scope, id, **kwargs,
        )

        self.lambda_function = aws_lambda.Function(
            self,
            "CeleryMetricsLambdaFunction",
            code=aws_lambda.Code.asset("awslambda"),
            handler="publish_celery_metrics.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            environment=scope.variables.regular_variables,
        )

        self.celery_default_cw_metric_schedule = events.Rule(
            self,
            "CeleryDefaultCWMetricSchedule",
            schedule=events.Schedule.rate(core.Duration.minutes(5)),
            targets=[
                events_targets.LambdaFunction(handler=self.lambda_function)
            ],
        )

        # TODO: refactor this to loop through CloudWatch metrics multiple celery queues
        scope.celery_default_service.default_celery_queue_cw_metric.grant_put_metric_data(
            scope.backend_service.backend_task.task_role
        )
