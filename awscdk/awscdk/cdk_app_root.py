from aws_cdk import core, aws_ecs as ecs

from cert import SiteCertificate
from hosted_zone import HostedZone
from cloudfront import CloudFront
from ecr import ElasticContainerRepo
from vpc import Vpc
from assets import Assets
from rds import Rds
from elasticache import ElastiCache
from alb import ApplicationLoadBalancer
from ecs import Ecs
from env_vars import Variables
from static_site_bucket import StaticSiteBucket

from backend import Backend
from backend_tasks import BackendTasks


class ApplicationStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        environment_name: str,
        base_domain_name: str,
        full_domain_name: str,
        base_app_name: str,
        full_app_name: str,
        **kwargs
    ) -> None:

        super().__init__(scope, id, **kwargs)

        self.hosted_zone = HostedZone(self, "HostedZone")

        self.certificate = SiteCertificate(
            self, "SiteCert", domain_name=full_domain_name
        )

        self.vpc = Vpc(self, "Vpc")

        self.alb = ApplicationLoadBalancer(
            self,
            "ApplicationLoadBalancer",
            hosted_zone=self.hosted_zone,
            certificate=self.certificate,
            vpc=self.vpc.vpc,
        )

        self.static_site_bucket = StaticSiteBucket(
            self, "StaticSiteBucket", full_app_name=full_app_name
        )

        self.cloudfront = CloudFront(
            self,
            "StaticSite",
            hosted_zone=self.hosted_zone,
            static_site_bucket_name=self.static_site_bucket.static_site_bucket.bucket_name,  # noqa
            certificate=self.certificate,
            alb=self.alb.alb.load_balancer_dns_name,
            full_domain_name=full_domain_name,
            full_app_name=full_app_name,
        )

        # TODO: remove this
        # self.ecr_repo = ElasticContainerRepo(
        #     self, "ElasticContainerRepo", full_app_name=full_app_name
        # )

        self.ecs = Ecs(
            self, "Ecs", vpc=self.vpc.vpc, full_app_name=full_app_name
        )

        self.assets = Assets(
            self, "BackendAssets", full_app_name=full_app_name
        )

        self.rds = Rds(
            self, "RdsDBCluster", vpc=self.vpc.vpc, full_app_name=full_app_name
        )

        self.elasticache = ElastiCache(
            self, "ElastiCacheRedis", vpc=self.vpc.vpc
        )

        # image used for all django containers
        # gunicorn, daphne, celery workers, celery beat
        self.image = ecs.AssetImage(
            "../backend", file="scripts/prod/Dockerfile", target="production",
        )

        self.variables = Variables(
            self,
            "Variables",
            bucket_name=self.assets.assets_bucket.bucket_name,
            db_secret=self.rds.db_secret,
            postgres_host=self.rds.rds_cluster.get_att(
                "Endpoint.Address"
            ).to_string(),
            redis_host=self.elasticache.elasticache.attr_redis_endpoint_address,  # noqa
        )

        self.backend = Backend(
            self,
            "Backend",
            image=self.image,
            load_balancer=self.alb,
            cluster=self.ecs.cluster,
            environment_variables=self.variables,
            security_group=self.vpc.vpc.vpc_default_security_group,
        )

        # migrate, collectstatic, createsuperuser
        self.backend_tasks = BackendTasks(
            self,
            "BackendTasks",
            image=self.image,
            cluster=self.ecs.cluster,
            environment_variables=self.variables,
            full_app_name=full_app_name,
        )

        # TODO: loop over all task roles to grant bucket permissions
        # give the backend service read/write access to the assets bucket
        task_roles = [
            self.backend.backend_task.task_role,
            self.backend_tasks.collectstatic_task.task_role,
            self.backend_tasks.create_superuser_task.task_role,
        ]

        for task_role in task_roles:
            self.assets.assets_bucket.grant_read_write(task_role)

            # TODO: Is this necessary? what is the best way to grant task
            # execution role to secrets?
            for secret in [
                self.variables.django_secret_key,
                self.rds.db_secret,
            ]:
                secret.grant_read(task_role)
