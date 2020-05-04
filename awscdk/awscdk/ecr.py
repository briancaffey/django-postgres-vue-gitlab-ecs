from aws_cdk import core, aws_ecr as ecr


class ElasticContainerRepo(ecr.Repository):
    def __init__(
        self, scope: core.Construct, id: str, domain_name: str, **kwargs
    ) -> None:
        super().__init__(
            scope, id, repository_name=f"{domain_name}/backend",
        )
