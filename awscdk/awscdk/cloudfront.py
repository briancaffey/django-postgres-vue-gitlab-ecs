from aws_cdk import (
    aws_certificatemanager as acm,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_route53 as route53,
    aws_iam as iam,
    aws_route53_targets as targets,
    core,
)


class CloudFront(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        hosted_zone: route53.IHostedZone,
        certificate: acm.ICertificate,
        alb: str,
        full_domain_name: str,
        full_app_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.static_site_bucket = s3.Bucket(
            self,
            "StaticSiteBucket",
            access_control=s3.BucketAccessControl.PUBLIC_READ,
            bucket_name=f"{full_app_name}-frontend",
            removal_policy=core.RemovalPolicy.DESTROY,
            website_index_document="index.html",
            website_error_document="index.html",
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

        path_patterns = ["/api/*", "/admin/*", "/flower/*"]
        self.distribution = cloudfront.CloudFrontWebDistribution(
            self,
            "CloudFrontDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    custom_origin_source=cloudfront.CustomOriginConfig(
                        domain_name=alb,
                        origin_protocol_policy=cloudfront.OriginProtocolPolicy.MATCH_VIEWER,
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            allowed_methods=cloudfront.CloudFrontAllowedMethods.ALL,
                            path_pattern=path_pattern,
                            forwarded_values={
                                "headers": ["*"],
                                "cookies": {"forward": "all"},
                                "query_string": True,
                            },
                        )
                        for path_pattern in path_patterns
                    ],
                ),
                cloudfront.SourceConfiguration(
                    custom_origin_source=cloudfront.CustomOriginConfig(
                        domain_name=f"{self.static_site_bucket.bucket_name}.s3-website-us-east-1.amazonaws.com",
                        origin_protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
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
                names=[full_domain_name],
            ),
        )

        route53.ARecord(
            self,
            "AliasRecord",
            target=route53.AddressRecordTarget.from_alias(
                targets.CloudFrontTarget(self.distribution)
            ),
            zone=hosted_zone.hosted_zone,
            record_name=f"{full_domain_name}.",
        )
