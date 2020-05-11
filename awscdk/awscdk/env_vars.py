from aws_cdk import core, aws_secretsmanager as secrets, aws_ecs as ecs


class Variables(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        bucket_name: str,
        postgres_host: str,
        db_secret: secrets.ISecret,
        **kwargs,
    ) -> None:
        super().__init__(
            scope, id, **kwargs,
        )

        self.regular_variables = {
            "DJANGO_SETTINGS_MODULE": "backend.settings.production",
            "DEBUG": "",
            "AWS_STORAGE_BUCKET_NAME": bucket_name,
            "POSTGRES_SERVICE_HOST": postgres_host,
            "POSTGRES_PASSWORD": db_secret.secret_value_from_json(
                "password"
            ).to_string(),
        }

        self.django_secret_key = secrets.Secret(
            self,
            "DjangoSecretKey",
            generate_secret_string=secrets.SecretStringGenerator(
                exclude_punctuation=True, include_space=False,
            ),
        )

        self.secret_variables = {
            "SECRET_KEY": ecs.Secret.from_secrets_manager(
                self.django_secret_key
            ),
        }
