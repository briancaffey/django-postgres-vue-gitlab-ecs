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

        self.listener = self.alb.add_listener(
            "ALBListener", port=80, open=True
        )

        self.https_listener = self.alb.add_listener(
            "HTTPSListener", port=443, certificates=[certificate]
        )

        # self.listener.add_redirect_response(
        #     'RedirectNonHttpsTraffic', status_code="HTTP_301", port="443"
        # )

        self.default_target_group = elbv2.ApplicationTargetGroup(
            self,
            "DefaultTargetGroup",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            vpc=vpc,
        )

        self.listener.add_target_groups(
            "DefaultTargetGroup", target_groups=[self.default_target_group]
        )

        self.https_listener.add_target_groups(
            "HTTPSDefaultTargetGroup",
            target_groups=[self.default_target_group],
        )
