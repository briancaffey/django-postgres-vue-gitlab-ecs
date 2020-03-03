# AWS CDK

## Setup

Here's a great workshop for getting started with AWS CDK:

[https://cdkworkshop.com/30-python.html](https://cdkworkshop.com/30-python.html)

Use a version of Node >= 10:

```sh
nvm use 13
Now using node v13.9.0 (npm v6.13.7)
```

Check the CDK version:

```sh
cdk --version
1.25.0 (build 5ced526)
```

:::warning Warning

deactivate pyenv with the following command:

```sh
pyenv local system
```

:::

### CDK init

Run `cdk init` in an empty directory:

```
cdk init app --language=python

cdk init app --language=python
Applying project template app for python
Executing Creating virtualenv...

# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

$ python3 -m venv .env

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

$ source .env/bin/activate

If you are a Windows platform, you would activate the virtualenv like this:

% .env\Scripts\activate.bat

Once the virtualenv is activated, you can install the required dependencies.

$ pip install -r requirements.txt

At this point you can now synthesize the CloudFormation template for this code.

$ cdk synth


To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
```

## Recreating the stack

In my current architecture I use the following resources:

1. ACM
1. Frontend Resources (S3 buckets, CloudFront distribution)
1. ECR
1. VPC
1. S3 Bucket for Django that ECS needs to be able to access
1. Service Role for ECS
1. Task Role for ECS
1. RDS
1. ElastiCache
1. ALB
1. ECS Cluster
1. ECS Services and Tasks

Let's try to replicate this component by component using CDK.

Remember, `cdk` generates CloudFormation templates or us. There is a one-to-one relationship between cdk stacks and CloudFormation stacks. We can use `cdk synth` to see what CloudFormation templates it will generate.

Here's the python reference for CDK:

[https://docs.aws.amazon.com/cdk/api/latest/python/index.html](https://docs.aws.amazon.com/cdk/api/latest/python/index.html)

### ACM Certificate

Let's start by getting a certificate. `DnsValidatedCertificate` looks like what we want.

Here's what I have in CloudFormation:

```
Description: >
  This template deploys a wildcard Amazon Certificate Manager (ACM) certificate.

Parameters:
  AppUrl:
    Type: "String"
    Description: "The URL for our app (e.g. mydomain.com)"
    AllowedPattern: "[a-z0-9._-]+"

  StackName:
    Type: String
    Description: The name of the stack

Resources:
  WildcardCertificate:
    Type: AWS::CertificateManager::Certificate
    Properties:
      DomainName: !Ref AppUrl
      SubjectAlternativeNames:
        - !Sub "*.${AppUrl}"
      DomainValidationOptions:
        - DomainName: !Ref AppUrl
          ValidationDomain: !Ref AppUrl
      ValidationMethod: DNS

Outputs:
  WildcardCert:
    Description: The Wildcard Certificate
    Value: !Ref WildcardCertificate
```

Here's the CDK code we need to generate this resource:

```python
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
            domain_name=f"*.{os.environ.get('DOMAIN_NAME', 'mysite.com')}",
            **kwargs
        )
```

### Frontend Resources

This next set of resources hosts our Vue.js site

Here are the records from the `static-site.yaml` template in `cloudformation/`:

1. StaticSiteBucket
1. StaticSiteBucketPolicy
1. CFDistribution
1. DNSRecord
1. WildCardDNSRecord

See `static_site.py` to see how we can generate these resources with AWS CDK.

### ECR (Elastic Container Registry)

Elastic Container Registry is a private container registry that will store our container images that are built in our CI/CD pipeline. ECS will pull images from this registry and use them to run containers.

Here's the CloudFormation used to create our existring ECR:

```
Description: >
  This template deploys an ECR Repository that we will use when pushing our backend container images.

Parameters:

  StackName:
    Type: String
    Description: The name of the stack

  ECRBackendRepositoryName:
    Type: "String"
    Description: "The name of the ECR Repository for our backend conainer."

Resources:
  ECRBackendRepository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: !Ref ECRBackendRepositoryName

Outputs:
  EcrBackendRepo:
    Description: The ECR Repository for the main backend container
    Value: !Sub "${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/${ECRBackendRepositoryName}"

```

For the `ECRBackendRepositoryName` I have been using `${AppUrl}/backend`, so we can use `f"{os.environ.get('DOMAIN_NAME')}/backend"`

Let's create `ecr.py` to create this resource with CDK:
