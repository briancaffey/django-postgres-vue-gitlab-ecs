#!/usr/bin/env python3
import os

from aws_cdk import core

from awscdk.cdk_app_root import ApplicationStack

# set domain name with DOMAIN_NAME and ENVIRONMENT
# example: dev.mydomain.com or app.mydomain.com
domain_name = os.environ.get("DOMAIN_NAME", "mysite.com")
environment = f"{os.environ.get('ENVIRONMENT', 'dev')}"
if not domain_name or not environment:
    raise Exception("Domain name or environment not set")
domain_name = f"{environment}.{domain_name}"


app = core.App()
ApplicationStack(
    app,
    f"cdk-app-{environment}",
    domain_name=domain_name,
    env={"region": "us-east-1"},
)

app.synth()
