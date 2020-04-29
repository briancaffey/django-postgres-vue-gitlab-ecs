from aws_cdk import core

from cert import SiteCertificate
from hosted_zone import HostedZone
from static_site import StaticSite
from ecr import ElasticContainerRepo
from vpc import Vpc
from assets import Assets
from rds import Rds
from elasticache import ElastiCache
from alb import ApplicationLoadBalancer
from ecs import Ecs

from backend import Backend


class AwscdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.hosted_zone = HostedZone(self, "HostedZone")

        self.certificate = SiteCertificate(self, "SiteCert")

        self.vpc = Vpc(self, "Vpc")

        self.alb = ApplicationLoadBalancer(
            self,
            "ApplicationLoadBalancer",
            hosted_zone=self.hosted_zone,
            certificate=self.certificate,
            vpc=self.vpc.vpc,
        )

        self.static_site = StaticSite(
            self,
            "StaticSite",
            hosted_zone=self.hosted_zone,
            certificate=self.certificate,
            alb=self.alb.alb.load_balancer_dns_name,
        )

        self.ecr_repo = ElasticContainerRepo(self, "ElasticContainerRepo")

        self.ecs = Ecs(self, "Ecs", vpc=self.vpc.vpc)

        self.backend = Backend(
            self, "Backend", load_balancer=self.alb, cluster=self.ecs.cluster
        )

        # self.assets = Assets(self, "BackendAssets")

        # self.rds = Rds(self, "RdsInstance", vpc=self.vpc.vpc)

        # self.elasticache = ElastiCache(self, "ElastiCacheRedis", vpc=self.vpc.vpc)

        # self.ecs = Ecs(
        #     self,
        #     "EcsResources",
        #     vpc=self.vpc.vpc,
        #     assets=self.assets
        # )
