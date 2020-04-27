import os

from aws_cdk import core, aws_ecr as ecr


class ElasticContainerRepo(ecr.Repository):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(
            scope,
            id,
            repository_name=f"{os.environ.get('DOMAIN_NAME', 'mysite.com')}/backend",
        )
