#!/usr/bin/env python3
import os

from aws_cdk import core

from awscdk.cdk_app_root import ApplicationStack

# naming conventions, also used for ACM certs, DNS Records, resource naming
# Dynamically generated resource names created in CDK are used in GitLab CI
# such as cluster name, task definitions, etc.
environment_name = f"{os.environ.get('ENVIRONMENT', 'dev')}"
base_domain_name = os.environ.get("DOMAIN_NAME", "mysite.com")
# if the the production environent subdomain should nott be included in the URL
# redefine `full_domain_name` to `base_domain_name` for that environment
full_domain_name = f"{environment_name}.{base_domain_name}"  # dev.mysite.com
if environment_name == "app":
    full_domain_name = base_domain_name
base_app_name = os.environ.get("APP_NAME", "mysite-com")
full_app_name = f"{environment_name}-{base_app_name}"  # dev-mysite-com
aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


app = core.App()
stack = ApplicationStack(
    app,
    f"{full_app_name}-stack",
    environment_name=environment_name,
    base_domain_name=base_domain_name,
    full_domain_name=full_domain_name,
    base_app_name=base_app_name,
    full_app_name=full_app_name,
    env={"region": aws_region},
)

# in order to be able to tag ECS resources, you need to go to
# the ECS Console > Account Settings > Amazon ECS ARN and resource ID settings
# and enable at least Service and Task. Optionally enable
# CloudWatch Container Insights
stack.node.apply_aspect(core.Tag("StackName", full_app_name))

app.synth()
