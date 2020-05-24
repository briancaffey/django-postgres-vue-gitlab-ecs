import os

from aws_cdk import (
    core,
    aws_certificatemanager as acm,
)


class SiteCertificate(acm.Certificate):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(
            scope,
            id,
            domain_name=scope.full_domain_name,
            validation_method=acm.ValidationMethod.DNS,
            **kwargs,
        )
