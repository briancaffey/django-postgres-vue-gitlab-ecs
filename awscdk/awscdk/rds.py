import json

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secrets,
    aws_ssm as ssm,
)


class Rds(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        domain_name: str,
        vpc: ec2.IVpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        app_name = domain_name.replace('.', '-')
        # secrets manager for DB password
        self.db_secret = secrets.Secret(
            self,
            "DBSecret",
            secret_name=f"{id}-{app_name}-secret",
            generate_secret_string=secrets.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "postgres"}),
                exclude_punctuation=True,
                include_space=False,
                generate_string_key="password",
            ),
        )

        self.db_secret_arn = ssm.StringParameter(
            self,
            'DBSecretArn',
            parameter_name=f"{app_name}-secret-arn",
            string_value=self.db_secret.secret_arn,
        )

        self.db_security_group = ec2.CfnSecurityGroup(
            self,
            "DBSecurityGroup",
            vpc_id=vpc.vpc_id,
            group_description="DBSecurityGroup",
            security_group_ingress=[
                ec2.CfnSecurityGroup.IngressProperty(
                    ip_protocol="tcp",
                    to_port=5432,
                    from_port=5432,
                    source_security_group_id=vpc.vpc_default_security_group,
                )
            ],
        )

        self.db_subnet_group = rds.CfnDBSubnetGroup(
            self,
            "CfnDBSubnetGroup",
            subnet_ids=vpc.select_subnets(
                subnet_type=ec2.SubnetType.ISOLATED
            ).subnet_ids,
            db_subnet_group_description=f"{domain_name}-db-subnet-group",
        )

        self.db_config = {
            "engine_mode": "serverless",
            "engine": "aurora-postgresql",
            "engine_version": "10.7",
            "port": 5432,
            "enable_http_endpoint": True,
            "master_username": self.db_secret.secret_value_from_json(
                "username"
            ).to_string(),
            "master_user_password": self.db_secret.secret_value_from_json(
                "password"
            ).to_string(),
            "vpc_security_group_ids": [
                self.db_security_group.get_att("GroupId").to_string()
            ],
            "db_subnet_group_name": self.db_security_group.ref,
        }

        self.rds_cluster = rds.CfnDBCluster(
            self, "DBCluster", **self.db_config
        )
