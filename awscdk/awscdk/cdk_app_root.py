from aws_cdk import core

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

from backend import Backend


class ApplicationStack(core.Stack):
    def __init__(
        self, scope: core.Construct, id: str, domain_name: str, **kwargs
    ) -> None:

        super().__init__(scope, id, **kwargs)

        self.hosted_zone = HostedZone(self, "HostedZone")

        self.certificate = SiteCertificate(
            self, "SiteCert", domain_name=domain_name
        )

        self.vpc = Vpc(self, "Vpc")

        self.alb = ApplicationLoadBalancer(
            self,
            "ApplicationLoadBalancer",
            hosted_zone=self.hosted_zone,
            certificate=self.certificate,
            vpc=self.vpc.vpc,
        )

        self.cloudfront = CloudFront(
            self,
            "StaticSite",
            hosted_zone=self.hosted_zone,
            certificate=self.certificate,
            alb=self.alb.alb.load_balancer_dns_name,
            domain_name=domain_name,
        )

        self.ecr_repo = ElasticContainerRepo(
            self, "ElasticContainerRepo", domain_name=domain_name
        )

        self.ecs = Ecs(self, "Ecs", vpc=self.vpc.vpc, domain_name=domain_name)

        self.backend = Backend(
            self,
            "Backend",
            load_balancer=self.alb,
            cluster=self.ecs.cluster,
            domain_name=domain_name,
        )

        self.assets = Assets(self, "BackendAssets", domain_name=domain_name)

        # give the backend service read/write access to the assets bucket
        self.assets.assets_bucket.grant_read_write(
            self.backend.backend_task.task_role
        )

        # self.rds = Rds(self, "RdsInstance", vpc=self.vpc.vpc)

        # self.elasticache = ElastiCache(
        #     self, "ElastiCacheRedis", vpc=self.vpc.vpc
        # )
