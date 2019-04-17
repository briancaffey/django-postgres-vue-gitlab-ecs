#!/usr/bin/env python3

import os
import json
import subprocess

secrets = []

variables = [
    'StackName',
    'SSHKeyName',
    'EnvironmentName',
    'AppUrl',
    'HostedZoneId',
    'SSLCertificateArn',
    'GitSHA',
    'ECRBackendRepositoryName',
    'WildcardSSLCertificateArn',
    'FlowerUsername',
    'FlowerPassword',
    'DjangoSecretKey',
    'AWSAccessKeyId',
    'AWSSecretAccessKey',
]

for v in variables:
    pair = {}
    pair['ParameterKey'] = v
    pair['ParameterValue'] = os.environ.get(v)
    secrets.append(pair)

with open('parameters.json', 'w+') as f:
    f.write(json.dumps(secrets, indent=4))
