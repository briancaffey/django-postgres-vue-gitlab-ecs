from aws_cdk import (
    aws_certificatemanager as acm,
    aws_cloudformation as cloudformation,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_route53 as route53,
    aws_iam as iam,
    aws_route53_targets as targets,
    core,
)

MATCH_VIEWER = cloudfront.OriginProtocolPolicy.MATCH_VIEWER
ALL_METHODS = cloudfront.CloudFrontAllowedMethods.ALL
HTTP_ONLY = cloudfront.OriginProtocolPolicy.HTTP_ONLY
GET_HEAD = cloudfront.CloudFrontAllowedMethods.GET_HEAD


class CloudFrontStack(cloudformation.NestedStack):
    def __init__(self, scope: core.Construct, id: str, **kwargs,) -> None:
        super().__init__(scope, id, **kwargs)

        s3_domain_prefix = scope.static_site_bucket.bucket_name
        s3_domain_suffix = ".s3-website-us-east-1.amazonaws.com"
        s3_website_domain_name = s3_domain_prefix + s3_domain_suffix

        path_patterns = ["/api/*", "/admin/*", "/flower/*"]

        self.distribution = cloudfront.CloudFrontWebDistribution(
            self,
            "CloudFrontDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    custom_origin_source=cloudfront.CustomOriginConfig(
                        domain_name=scope.alb.load_balancer_dns_name,
                        origin_protocol_policy=MATCH_VIEWER,
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            allowed_methods=ALL_METHODS,
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
                        domain_name=s3_website_domain_name,
                        origin_protocol_policy=HTTP_ONLY,
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            is_default_behavior=True, cached_methods=GET_HEAD,
                        )
                    ],
                ),
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=scope.backend_assets_bucket
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            allowed_methods=ALL_METHODS,
                            forwarded_values={"query_string": True},
                            path_pattern=path_pattern,
                            min_ttl=core.Duration.seconds(0),
                            default_ttl=core.Duration.seconds(0),
                            max_ttl=core.Duration.seconds(0),
                        )
                        for path_pattern in ["/static/*", "/media/*"]
                    ],
                ),
            ],
            alias_configuration=cloudfront.AliasConfiguration(
                acm_cert_ref=scope.certificate.certificate_arn,
                names=[scope.full_domain_name],
            ),
        )

        route53.ARecord(
            self,
            "AliasRecord",
            target=route53.AddressRecordTarget.from_alias(
                targets.CloudFrontTarget(self.distribution)
            ),
            zone=scope.hosted_zone,
            record_name=f"{scope.full_domain_name}.",
        )
