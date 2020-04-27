from aws_cdk import (
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_route53 as route53,
    aws_certificatemanager as acm,
    aws_elasticloadbalancingv2 as elbv2,
    core,
)


class ApplicationLoadBalancer(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        hosted_zone: route53.IHostedZone,
        certificate: acm.ICertificate,
        vpc: ec2.IVpc,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.alb = elbv2.ApplicationLoadBalancer(
            self, "ALB", internet_facing=True, vpc=vpc
        )

        self.alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80"
        )

        self.alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(443), "Internet access ALB 443"
        )

        redirect_listener = elbv2.CfnListener(
            self,
            "RedirectListener",
            protocol="HTTP",
            port=80,
            load_balancer_arn=self.alb.load_balancer_arn,
            default_actions=[
                {
                    "type": "redirect",
                    "redirectConfig": {
                        "host": "#{host}",
                        "path": "/#{path}",
                        "port": "443",
                        "protocol": "HTTPS",
                        "query": "#{query}",
                        "statusCode": "HTTP_301",
                    },
                }
            ],
        )

        self.default_target_group = elbv2.CfnTargetGroup(
            self, "DefaultTargetGroup", vpc_id=vpc.vpc_id, port=80, protocol="HTTP"
        )

        self.https_listener = elbv2.CfnListener(
            self,
            "HttpsListener",
            protocol="HTTPS",
            port=443,
            load_balancer_arn=self.alb.load_balancer_arn,
            certificates=[{"certificateArn": certificate.certificate_arn}],
            default_actions=[
                {
                    "targetGroupArn": self.default_target_group.get_att(
                        "TargetGroupFullName"
                    ).to_string(),
                    "type": "forward",
                }
            ],
        )
