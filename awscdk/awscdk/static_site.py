import os

from aws_cdk import (
    aws_certificatemanager as acm,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_route53 as route53,
    aws_iam as iam,
    aws_route53_targets as targets,
    core,
)


class StaticSite(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        hosted_zone: route53.IHostedZone,
        certificate: acm.ICertificate,
        alb: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.static_site_bucket = s3.Bucket(
            self,
            "StaticSiteBucket",
            access_control=s3.BucketAccessControl.PUBLIC_READ,
            bucket_name=os.environ.get("DOMAIN_NAME", "mysite.com"),
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        self.policy_statement = iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"{self.static_site_bucket.bucket_arn}/*"],
        )

        self.policy_statement.add_any_principal()

        self.static_site_policy_document = iam.PolicyDocument(
            statements=[self.policy_statement]
        )

        self.static_site_bucket.add_to_resource_policy(self.policy_statement)

        self.distribution = cloudfront.CloudFrontWebDistribution(
            self,
            "CloudFrontDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    custom_origin_source=cloudfront.CustomOriginConfig(
                        domain_name=alb,
                        origin_protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            allowed_methods=cloudfront.CloudFrontAllowedMethods.ALL,
                            path_pattern="/api/*",
                            forwarded_values={
                                "headers": ["*"],
                                "cookies": {"forward": "all"},
                                "query_string": True,
                            },
                        )
                    ],
                ),
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=self.static_site_bucket
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            is_default_behavior=True,
                            cached_methods=cloudfront.CloudFrontAllowedMethods.GET_HEAD,
                        )
                    ],
                ),
            ],
            alias_configuration=cloudfront.AliasConfiguration(
                acm_cert_ref=certificate.certificate_arn,
                names=[
                    os.environ.get("DOMAIN_NAME", "mysite.com"),
                    f"*.{os.environ.get('DOMAIN_NAME', 'mysite.com')}",
                ],
            ),
            error_configurations=[
                {
                    "errorCode": 403,
                    "errorCachingMinTtl": 0,
                    "responseCode": 200,
                    "responsePagePath": "/index.html",
                },
                {
                    "errorCode": 404,
                    "errorCachingMinTtl": 0,
                    "responseCode": 200,
                    "responsePagePath": "/index.html",
                },
            ],
        )

        route53.ARecord(
            self,
            "AliasRecord",
            target=route53.AddressRecordTarget.from_alias(
                targets.CloudFrontTarget(self.distribution)
            ),
            zone=hosted_zone.hosted_zone,
            # don't forget the '.' at the end of the record name!
            record_name=f"*.{os.environ.get('DOMAIN_NAME', 'mysite.com')}.",
        )

        route53.ARecord(
            self,
            "AliasRecord1",
            target=route53.AddressRecordTarget.from_alias(
                targets.CloudFrontTarget(self.distribution)
            ),
            zone=hosted_zone.hosted_zone,
            # don't forget the '.' at the end of the record name!
            record_name=f"{os.environ.get('DOMAIN_NAME', 'mysite.com')}.",
        )
