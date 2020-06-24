import os

from aws_cdk import core, aws_secretsmanager as secrets, aws_ecs as ecs


class Variables(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        bucket_name: str,
        postgres_host: str,
        redis_host: str,
        db_secret: secrets.ISecret,
        full_domain_name: str,
        **kwargs,
    ) -> None:
        super().__init__(
            scope, id, **kwargs,
        )

        self.django_secret_key = secrets.Secret(
            self,
            "DjangoSecretKey",
            generate_secret_string=secrets.SecretStringGenerator(
                exclude_punctuation=True, include_space=False,
            ),
        )

        self.regular_variables = {
            "DJANGO_SETTINGS_MODULE": "backend.settings.production",
            "DEBUG": "",
            "FULL_DOMAIN_NAME": full_domain_name,
            "FULL_APP_NAME": scope.full_app_name,
            "CELERY_METRICS_TOKEN": "my-secret-token",
            "AWS_STORAGE_BUCKET_NAME": bucket_name,
            "POSTGRES_SERVICE_HOST": postgres_host,
            "POSTGRES_PASSWORD": db_secret.secret_value_from_json(
                "password"
            ).to_string(),
            "SECRET_KEY": os.environ.get(
                "SECRET_KEY", "mysecretkey123"
            ),  # self.django_secret_key.to_string(),
            "REDIS_SERVICE_HOST": redis_host,
        }

        self.secret_variables = {
            "DJANGO_SECRET_KEY": ecs.Secret.from_secrets_manager(
                self.django_secret_key
            ),
        }
