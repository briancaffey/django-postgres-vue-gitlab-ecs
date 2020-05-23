import os

from aws_cdk import (
    core,
    aws_ecs as ecs,
)


class BackendTasks(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        image: ecs.AssetImage,
        cluster: ecs.ICluster,
        environment_variables: core.Construct,
        full_app_name: str,
        **kwargs,
    ) -> None:
        super().__init__(
            scope, id, **kwargs,
        )

        self.migrate_task = ecs.FargateTaskDefinition(
            self, "MigrateTask", family=f"{full_app_name}-migrate"
        )

        for secret in [scope.variables.django_secret_key, scope.rds.db_secret]:
            secret.grant_read(self.migrate_task.task_role)

        self.migrate_task.add_container(
            "MigrateCommand",
            image=image,
            environment=environment_variables.regular_variables,
            secrets=environment_variables.secret_variables,
            command=["python3", "manage.py", "migrate", "--no-input"],
            logging=ecs.LogDrivers.aws_logs(stream_prefix="MigrateCommand"),
        )

        self.collectstatic_task = ecs.FargateTaskDefinition(
            self, "CollecstaticTask", family=f"{full_app_name}-collectstatic"
        )

        scope.assets.assets_bucket.grant_read_write(
            self.collectstatic_task.task_role
        )

        for secret in [scope.variables.django_secret_key, scope.rds.db_secret]:
            secret.grant_read(self.collectstatic_task.task_role)

        self.collectstatic_task.add_container(
            "CollecstaticCommand",
            image=image,
            environment=environment_variables.regular_variables,
            secrets=environment_variables.secret_variables,
            command=["python3", "manage.py", "collectstatic", "--no-input"],
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="CollectstaticCommand"
            ),
        )

        self.create_superuser_task = ecs.FargateTaskDefinition(
            self,
            "CreateSuperuserTask",
            family=f"{full_app_name}-create-superuser",
        )

        for secret in [scope.variables.django_secret_key, scope.rds.db_secret]:
            secret.grant_read(self.create_superuser_task.task_role)

        self.create_superuser_task.add_container(
            "CreateSuperuserCommand",
            image=image,
            environment=environment_variables.regular_variables,
            secrets=environment_variables.secret_variables.update(
                {
                    "SUPERUSER_PASSWORD": os.environ.get(
                        "SUPERUSER_PASSWORD", "password"
                    )
                }
            ),
            command=["python3", "manage.py", "create_default_user"],
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="CreateSuperuserCommand"
            ),
        )
