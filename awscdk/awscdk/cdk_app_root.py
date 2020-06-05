import os

from aws_cdk import core, aws_ecs as ecs, aws_s3_deployment as s3_deployment

from alb import AlbStack
from backend_assets import BackendAssetsStack
from cert import SiteCertificate
from hosted_zone import HostedZone
from cloudfront import CloudFrontStack
from vpc import VpcStack
from rds import RdsStack
from elasticache import ElastiCacheStack
from ecs import EcsStack
from env_vars import Variables
from static_site_bucket import StaticSiteStack
from flower import FlowerServiceStack
from celery_autoscaling import CeleryAutoscalingStack

from backend import BackendServiceStack
from backend_tasks import BackendTasksStack
from celery_default import CeleryDefaultServiceStack


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

        self.environment_name = environment_name
        self.base_domain_name = base_domain_name
        self.full_domain_name = full_domain_name
        self.base_app_name = base_app_name
        self.full_app_name = full_app_name

        self.hosted_zone = HostedZone(self, "HostedZone").hosted_zone

        self.certificate = SiteCertificate(self, "SiteCert")

        self.vpc_stack = VpcStack(self, "VpcStack")
        self.vpc = self.vpc_stack.vpc

        self.alb_stack = AlbStack(self, "AlbStack")
        self.alb = self.alb_stack.alb

        self.https_listener = self.alb_stack.https_listener

        self.static_site_stack = StaticSiteStack(self, "StaticSiteStack")
        self.static_site_bucket = self.static_site_stack.static_site_bucket

        self.backend_assets = BackendAssetsStack(self, "BackendAssetsStack")
        self.backend_assets_bucket = self.backend_assets.assets_bucket

        self.cloudfront = CloudFrontStack(self, "CloudFrontStack")

        if os.path.isdir("./quasar/dist/pwa"):
            s3_deployment.BucketDeployment(
                self,
                "BucketDeployment",
                destination_bucket=self.static_site_bucket,
                sources=[s3_deployment.Source.asset("./quasar/dist/pwa")],
                distribution=self.cloudfront.distribution,
            )

        self.ecs = EcsStack(self, "EcsStack")
        self.cluster = self.ecs.cluster

        self.rds = RdsStack(self, "RdsStack")

        self.elasticache = ElastiCacheStack(self, "ElastiCacheStack")

        # image used for all django containers: gunicorn, daphne, celery, beat
        self.image = ecs.AssetImage(
            "./backend", file="scripts/prod/Dockerfile", target="production",
        )

        self.variables = Variables(
            self,
            "Variables",
            bucket_name=self.backend_assets_bucket.bucket_name,
            db_secret=self.rds.db_secret,
            full_domain_name=self.full_domain_name,
            postgres_host=self.rds.rds_cluster.get_att(
                "Endpoint.Address"
            ).to_string(),
            redis_host=self.elasticache.elasticache.attr_redis_endpoint_address,  # noqa
        )

        self.backend_service = BackendServiceStack(self, "BackendServiceStack")
        self.flower_service = FlowerServiceStack(self, "FlowerServiceStack")

        self.celery_default_service = CeleryDefaultServiceStack(
            self, "CeleryDefaultServiceStack"
        )

        # define other celery queues here, or combine in a single construct

        self.celery_autoscaling = CeleryAutoscalingStack(
            self, "CeleryAutoscalingStack"
        )

        # migrate, collectstatic, createsuperuser
        self.backend_tasks = BackendTasksStack(self, "BackendTasksStack")
