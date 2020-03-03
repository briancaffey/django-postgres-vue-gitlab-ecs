from aws_cdk import core

from cert import SiteCertificate
from hosted_zone import HostedZone
from static_site import StaticSite


class AwscdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.hosted_zone = HostedZone(self, "HostedZone")

        self.certificate = SiteCertificate(self, "SiteCert")

        self.static_site = StaticSite(
            self, 'StaticSite',
            hosted_zone=self.hosted_zone,
            certificate=self.certificate
        )
