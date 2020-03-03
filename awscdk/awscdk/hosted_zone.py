import os

from aws_cdk import (
    core,
    aws_route53 as route53
)


class HostedZone(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "hosted_zone",
            hosted_zone_id=os.environ.get("HOSTED_ZONE_ID", "ABC123"),
            zone_name=os.environ.get("DOMAIN_NAME", "mysite.com")
        )
