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
1. ECS Services
1. ECS Tasks (migrate, collectstatic)

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

```python
import os

from aws_cdk import (
    core,
    aws_ecr as ecr
)


class ElasticContainerRepo(ecr.Repository):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(
            scope,
            id,
            repository_name=\
                f"{os.environ.get('DOMAIN_NAME', 'mysite.com')}/backend"
        )
```

### VPC (Virtual Private Cloud)

Next let's create the VPC for our application.

Here are the resources that are defined in our `vpc.yaml` CloudFormation template:

1. VPC
1. PublicSubnetOne
1. PublicSubnetTwo
1. PrivateSubnetOne
1. PrivateSubnetTwo
1. InternetGateway
1. GatewayAttachment
1. PublicRouteTable
1. PublicRoute
1. PublicSubnetOneRouteTableAssociation
1. PublicSubnetTwoRouteTableAssociation

Here's the CDK code we need to generate these resources:

```python
from aws_cdk import core

from aws_cdk import (
    aws_ec2 as ec2
)


class Vpc(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "Vpc",
            max_azs=2,
            cidr="10.0.0.0/16",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.ISOLATED,
                    name="Isolated",
                    cidr_mask=24
                )
            ]
        )
```

Here's the output from our CDK VPC resource:

```yaml
VpcC3027511:
  Type: AWS::EC2::VPC
  Properties:
    CidrBlock: 10.0.0.0/16
    EnableDnsHostnames: true
    EnableDnsSupport: true
    InstanceTenancy: default
    Tags:
      - Key: Name
        Value: awscdk/Vpc/Vpc
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/Resource

VpcPublicSubnet1Subnet8E8DEDC0:
  Type: AWS::EC2::Subnet
  Properties:
    CidrBlock: 10.0.0.0/24
    VpcId:
      Ref: VpcC3027511
    AvailabilityZone:
      Fn::Select:
        - 0
        - Fn::GetAZs: ""
    MapPublicIpOnLaunch: true
    Tags:
      - Key: Name
        Value: awscdk/Vpc/Vpc/PublicSubnet1
      - Key: aws-cdk:subnet-name
        Value: Public
      - Key: aws-cdk:subnet-type
        Value: Public
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/PublicSubnet1/Subnet

VpcPublicSubnet1RouteTable431DD755:
  Type: AWS::EC2::RouteTable
  Properties:
    VpcId:
      Ref: VpcC3027511
    Tags:
      - Key: Name
        Value: awscdk/Vpc/Vpc/PublicSubnet1
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/PublicSubnet1/RouteTable

VpcPublicSubnet1RouteTableAssociationBBCB7AA1:
  Type: AWS::EC2::SubnetRouteTableAssociation
  Properties:
    RouteTableId:
      Ref: VpcPublicSubnet1RouteTable431DD755
    SubnetId:
      Ref: VpcPublicSubnet1Subnet8E8DEDC0
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/PublicSubnet1/RouteTableAssociation

VpcPublicSubnet1DefaultRoute0F5C6C43:
  Type: AWS::EC2::Route
  Properties:
    RouteTableId:
      Ref: VpcPublicSubnet1RouteTable431DD755
    DestinationCidrBlock: 0.0.0.0/0
    GatewayId:
      Ref: VpcIGW488B0FEB
  DependsOn:
    - VpcVPCGW42EC8516
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/PublicSubnet1/DefaultRoute

VpcPublicSubnet2SubnetA811849C:
  Type: AWS::EC2::Subnet
  Properties:
    CidrBlock: 10.0.1.0/24
    VpcId:
      Ref: VpcC3027511
    AvailabilityZone:
      Fn::Select:
        - 1
        - Fn::GetAZs: ""
    MapPublicIpOnLaunch: true
    Tags:
      - Key: Name
        Value: awscdk/Vpc/Vpc/PublicSubnet2
      - Key: aws-cdk:subnet-name
        Value: Public
      - Key: aws-cdk:subnet-type
        Value: Public
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/PublicSubnet2/Subnet

VpcPublicSubnet2RouteTable77FB35FC:
  Type: AWS::EC2::RouteTable
  Properties:
    VpcId:
      Ref: VpcC3027511
    Tags:
      - Key: Name
        Value: awscdk/Vpc/Vpc/PublicSubnet2
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/PublicSubnet2/RouteTable

VpcPublicSubnet2RouteTableAssociation3AFE92E6:
  Type: AWS::EC2::SubnetRouteTableAssociation
  Properties:
    RouteTableId:
      Ref: VpcPublicSubnet2RouteTable77FB35FC
    SubnetId:
      Ref: VpcPublicSubnet2SubnetA811849C
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/PublicSubnet2/RouteTableAssociation

VpcPublicSubnet2DefaultRouteD629179A:
  Type: AWS::EC2::Route
  Properties:
    RouteTableId:
      Ref: VpcPublicSubnet2RouteTable77FB35FC
    DestinationCidrBlock: 0.0.0.0/0
    GatewayId:
      Ref: VpcIGW488B0FEB
  DependsOn:
    - VpcVPCGW42EC8516
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/PublicSubnet2/DefaultRoute

VpcIGW488B0FEB:
  Type: AWS::EC2::InternetGateway
  Properties:
    Tags:
      - Key: Name
        Value: awscdk/Vpc/Vpc
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/IGW

VpcVPCGW42EC8516:
  Type: AWS::EC2::VPCGatewayAttachment
  Properties:
    VpcId:
      Ref: VpcC3027511
    InternetGatewayId:
      Ref: VpcIGW488B0FEB
  Metadata:
    aws:cdk:path: awscdk/Vpc/Vpc/VPCGW
```

### Assets bucket (for our Django backend)

Next let's add the resources for our Django assets. These assets are described in the `django-assets.yaml` CloudFormation template:

```yaml
Resources:
  AssetsBucket:
    Type: "AWS::S3::Bucket"
    Properties:
      BucketName: !Sub ${StackName}-assets

  AssetsBucketPolicy:
    Type: "AWS::S3::BucketPolicy"
    Properties:
      Bucket: !Ref AssetsBucket
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Sid: PublicReadForGetBucketObjects
            Effect: "Allow"
            Principal: "*"
            Action: "s3:GetObject"
            Resource: !Sub "${AssetsBucket.Arn}/static/*"
```

We need a bucket and a bucket policy.

Here's the CDK code needed to create these resources:

```python
from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    core
)


class Assets(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.assets_bucket = s3.Bucket(self, "AssetsBucket")

        self.policy_statement = iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"{self.assets_bucket.bucket_arn}/static/*"]
        )

        self.policy_statement.add_any_principal()

        self.static_site_policy_document = iam.PolicyDocument(
            statements=[self.policy_statement]
        )

        self.assets_bucket.add_to_resource_policy(
            self.policy_statement
        )

```

### Service Role for ECS

CDK generates this for us automatically.

### Task Execution Role for ECS Services

CDK also generates this for us automatically, but we need to extend it with `add_to_execution_role_policy(statement)` so that our tasks can access parameters stored in parameter store.

### RDS (Postgres Database)

Next let's add the RDS resources:

1. DatabaseSecurityGroup (AWS::EC2::SecurityGroup)
1. DBSubnetGroup (AWS::RDS::DBSubnetGroup)
1. RDSPostgres (AWS::RDS::DBInstance)

Here's the CDK to generate our RDS resources:

```python
import os

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_ssm as ssm
)

class Rds(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        vpc: ec2.IVpc,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.rds = rds.DatabaseInstance(
            self,
            "RdsInstance",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            master_username="postgres",
            instance_class=ec2.InstanceType(instance_type_identifier="t2.small"),
            vpc=vpc,
            vpc_placement=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.ISOLATED
            )
        )
```

This generates the following CloudFormation:

```yaml
RdsInstanceSubnetGroup719E4966:
  Type: AWS::RDS::DBSubnetGroup
  Properties:
    DBSubnetGroupDescription: Subnet group for RdsInstance database
    SubnetIds:
      - Ref: VpcIsolatedSubnet1SubnetDC3C6AF8
      - Ref: VpcIsolatedSubnet2SubnetB479B99C
  Metadata:
    aws:cdk:path: awscdk/RdsInstance/RdsInstance/SubnetGroup
RdsInstanceSecurityGroup66DE6329:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: Security group for RdsInstance database
    SecurityGroupEgress:
      - CidrIp: 0.0.0.0/0
        Description: Allow all outbound traffic by default
        IpProtocol: "-1"
    VpcId:
      Ref: VpcC3027511
  Metadata:
    aws:cdk:path: awscdk/RdsInstance/RdsInstance/SecurityGroup/Resource
RdsInstanceSecret62D934D7:
  Type: AWS::SecretsManager::Secret
  Properties:
    GenerateSecretString:
      ExcludeCharacters: '"@/\'
      GenerateStringKey: password
      PasswordLength: 30
      SecretStringTemplate: '{"username":"postgres"}'
  Metadata:
    aws:cdk:path: awscdk/RdsInstance/RdsInstance/Secret/Resource
RdsInstanceSecretAttachment67DB0F47:
  Type: AWS::SecretsManager::SecretTargetAttachment
  Properties:
    SecretId:
      Ref: RdsInstanceSecret62D934D7
    TargetId:
      Ref: RdsInstanceE36C7CB6
    TargetType: AWS::RDS::DBInstance
  Metadata:
    aws:cdk:path: awscdk/RdsInstance/RdsInstance/Secret/Attachment/Resource
RdsInstanceE36C7CB6:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceClass: db.t2.small
    AllocatedStorage: "100"
    CopyTagsToSnapshot: true
    DBSubnetGroupName:
      Ref: RdsInstanceSubnetGroup719E4966
    DeletionProtection: true
    Engine: postgres
    MasterUsername:
      Fn::Join:
        - ""
        - - "{{resolve:secretsmanager:"
          - Ref: RdsInstanceSecret62D934D7
          - :SecretString:username::}}
    MasterUserPassword:
      Fn::Join:
        - ""
        - - "{{resolve:secretsmanager:"
          - Ref: RdsInstanceSecret62D934D7
          - :SecretString:password::}}
    PubliclyAccessible: false
    StorageType: gp2
    VPCSecurityGroups:
      - Fn::GetAtt:
          - RdsInstanceSecurityGroup66DE6329
          - GroupId
  UpdateReplacePolicy: Retain
  DeletionPolicy: Retain
  Metadata:
    aws:cdk:path: awscdk/RdsInstance/RdsInstance/Resource
```

### ElastiCache (Redis)

ElastiCache doesn't have any high-level constucts in CDK, but we can still use CDK to generate CloudFormation for our ElastiCache resources.

(Javacript example: https://github.com/aws-samples/aws-cdk-changelogs-demo/blob/6fa3f6d9372d3502c8ceb8602c62acd51e63cd99/custom-constructs/redis.js)

We need to generate the following resources:

1. ElastiCacheSecurityGroup
1. ElastiCacheSubnetGroup
1. ElastiCacheCluster

```python
import os

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_elasticache as elasticache,
)


class ElastiCache(core.Construct):
    def __init__(self, scope: core.Construct, id: str, vpc: ec2.IVpc, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.elasticache_security_group = ec2.CfnSecurityGroup(
            self,
            "ElastiCacheSecurityGroup",
            vpc_id=vpc.vpc_id,
            group_description="ElastiCacheSecurityGroup",
            security_group_ingress=[ec2.CfnSecurityGroup.IngressProperty(
                ip_protocol="tcp",
                to_port=6379,
                from_port=6379,
                # TODO: replace this with ECS security group
                source_security_group_id="security-group-id"
            )]
        )

        self.elasticache_subnet_group = elasticache.CfnSubnetGroup(
            self, "CfnSubnetGroup",
            subnet_ids=vpc.select_subnets(
                subnet_type=ec2.SubnetType.ISOLATED
            ).subnet_ids,
            description="The subnet group for ElastiCache"
        )

        self.elasticache = elasticache.CfnCacheCluster(
            self,
            "ElastiCacheClusterRedis",
            cache_node_type="cache.t2.micro",
            engine="redis",
            num_cache_nodes=1,
            vpc_security_group_ids=[
                self.elasticache_security_group.get_att("GroupId").to_string()
            ],
            cache_subnet_group_name=self.elasticache_subnet_group.cache_subnet_group_name
        )
```

### Application Load Balancer

```yaml
ApplicationLoadBalancerALBE88818A8:
  Type: AWS::ElasticLoadBalancingV2::LoadBalancer
  Properties:
    Scheme: internet-facing
    SecurityGroups:
      - Fn::GetAtt:
          - ApplicationLoadBalancerALBSecurityGroup0D676F12
          - GroupId
    Subnets:
      - Ref: VpcPublicSubnet1Subnet8E8DEDC0
      - Ref: VpcPublicSubnet2SubnetA811849C
    Type: application
  DependsOn:
    - VpcPublicSubnet1DefaultRoute0F5C6C43
    - VpcPublicSubnet2DefaultRouteD629179A
  Metadata:
    aws:cdk:path: awscdk/ApplicationLoadBalancer/ALB/Resource
ApplicationLoadBalancerALBSecurityGroup0D676F12:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: Automatically created Security Group for ELB awscdkApplicationLoadBalancerALB81FD6B77
    SecurityGroupEgress:
      - CidrIp: 255.255.255.255/32
        Description: Disallow all traffic
        FromPort: 252
        IpProtocol: icmp
        ToPort: 86
    SecurityGroupIngress:
      - CidrIp: 0.0.0.0/0
        Description: Internet access ALB 80
        FromPort: 80
        IpProtocol: tcp
        ToPort: 80
      - CidrIp: 0.0.0.0/0
        Description: Internet access ALB 443
        FromPort: 443
        IpProtocol: tcp
        ToPort: 443
    VpcId:
      Ref: VpcC3027511
  Metadata:
    aws:cdk:path: awscdk/ApplicationLoadBalancer/ALB/SecurityGroup/Resource
```

### ECS Cluster

```yaml
EcsResourcesEcsClusterD9504452:
  Type: AWS::ECS::Cluster
  Metadata:
    aws:cdk:path: awscdk/EcsResources/EcsCluster/Resource
EcsResourcesAutoScalingGroupInstanceSecurityGroupE16CAB00:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: awscdk/EcsResources/AutoScalingGroup/InstanceSecurityGroup
    SecurityGroupEgress:
      - CidrIp: 0.0.0.0/0
        Description: Allow all outbound traffic by default
        IpProtocol: "-1"
    Tags:
      - Key: Name
        Value: awscdk/EcsResources/AutoScalingGroup
    VpcId:
      Ref: VpcC3027511
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/InstanceSecurityGroup/Resource
EcsResourcesAutoScalingGroupInstanceRole1D938B82:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Statement:
        - Action: sts:AssumeRole
          Effect: Allow
          Principal:
            Service: ec2.amazonaws.com
      Version: "2012-10-17"
    Tags:
      - Key: Name
        Value: awscdk/EcsResources/AutoScalingGroup
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/InstanceRole/Resource
EcsResourcesAutoScalingGroupInstanceRoleDefaultPolicyBB649C08:
  Type: AWS::IAM::Policy
  Properties:
    PolicyDocument:
      Statement:
        - Action:
            - ecs:CreateCluster
            - ecs:DeregisterContainerInstance
            - ecs:DiscoverPollEndpoint
            - ecs:Poll
            - ecs:RegisterContainerInstance
            - ecs:StartTelemetrySession
            - ecs:Submit*
            - ecr:GetAuthorizationToken
            - logs:CreateLogStream
            - logs:PutLogEvents
          Effect: Allow
          Resource: "*"
      Version: "2012-10-17"
    PolicyName: EcsResourcesAutoScalingGroupInstanceRoleDefaultPolicyBB649C08
    Roles:
      - Ref: EcsResourcesAutoScalingGroupInstanceRole1D938B82
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/InstanceRole/DefaultPolicy/Resource
EcsResourcesAutoScalingGroupInstanceProfileC59956DA:
  Type: AWS::IAM::InstanceProfile
  Properties:
    Roles:
      - Ref: EcsResourcesAutoScalingGroupInstanceRole1D938B82
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/InstanceProfile
EcsResourcesAutoScalingGroupLaunchConfigD1267A6F:
  Type: AWS::AutoScaling::LaunchConfiguration
  Properties:
    ImageId:
      Ref: SsmParameterValueawsserviceecsoptimizedamiamazonlinux2recommendedimageidC96584B6F00A464EAD1953AFF4B05118Parameter
    InstanceType: t2.micro
    IamInstanceProfile:
      Ref: EcsResourcesAutoScalingGroupInstanceProfileC59956DA
    SecurityGroups:
      - Fn::GetAtt:
          - EcsResourcesAutoScalingGroupInstanceSecurityGroupE16CAB00
          - GroupId
    UserData:
      Fn::Base64:
        Fn::Join:
          - ""
          - - >-
              #!/bin/bash

              echo ECS_CLUSTER=
            - Ref: EcsResourcesEcsClusterD9504452
            - >2-
                 >> /etc/ecs/ecs.config
                sudo iptables --insert FORWARD 1 --in-interface docker+ --destination 169.254.169.254/32 --jump DROP

                sudo service iptables save

                echo ECS_AWSVPC_BLOCK_IMDS=true >> /etc/ecs/ecs.config
  DependsOn:
    - EcsResourcesAutoScalingGroupInstanceRoleDefaultPolicyBB649C08
    - EcsResourcesAutoScalingGroupInstanceRole1D938B82
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/LaunchConfig
EcsResourcesAutoScalingGroupASG32373EB9:
  Type: AWS::AutoScaling::AutoScalingGroup
  Properties:
    MaxSize: "1"
    MinSize: "1"
    DesiredCapacity: "1"
    LaunchConfigurationName:
      Ref: EcsResourcesAutoScalingGroupLaunchConfigD1267A6F
    Tags:
      - Key: Name
        PropagateAtLaunch: true
        Value: awscdk/EcsResources/AutoScalingGroup
    VPCZoneIdentifier:
      - Ref: VpcPublicSubnet1Subnet8E8DEDC0
      - Ref: VpcPublicSubnet2SubnetA811849C
  UpdatePolicy:
    AutoScalingReplacingUpdate:
      WillReplace: true
    AutoScalingScheduledAction:
      IgnoreUnmodifiedGroupSizeProperties: true
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/ASG
EcsResourcesAutoScalingGroupDrainECSHookFunctionServiceRoleF2B1D493:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Statement:
        - Action: sts:AssumeRole
          Effect: Allow
          Principal:
            Service: lambda.amazonaws.com
      Version: "2012-10-17"
    ManagedPolicyArns:
      - Fn::Join:
          - ""
          - - "arn:"
            - Ref: AWS::Partition
            - :iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    Tags:
      - Key: Name
        Value: awscdk/EcsResources/AutoScalingGroup
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/DrainECSHook/Function/ServiceRole/Resource
? EcsResourcesAutoScalingGroupDrainECSHookFunctionServiceRoleDefaultPolicy039D81DC
: Type: AWS::IAM::Policy
  Properties:
    PolicyDocument:
      Statement:
        - Action:
            - ec2:DescribeInstances
            - ec2:DescribeInstanceAttribute
            - ec2:DescribeInstanceStatus
            - ec2:DescribeHosts
          Effect: Allow
          Resource: "*"
        - Action: autoscaling:CompleteLifecycleAction
          Effect: Allow
          Resource:
            Fn::Join:
              - ""
              - - "arn:"
                - Ref: AWS::Partition
                - ":autoscaling:us-east-1:"
                - Ref: AWS::AccountId
                - :autoScalingGroup:*:autoScalingGroupName/
                - Ref: EcsResourcesAutoScalingGroupASG32373EB9
        - Action:
            - ecs:DescribeContainerInstances
            - ecs:DescribeTasks
          Effect: Allow
          Resource: "*"
        - Action:
            - ecs:ListContainerInstances
            - ecs:SubmitContainerStateChange
            - ecs:SubmitTaskStateChange
          Effect: Allow
          Resource:
            Fn::GetAtt:
              - EcsResourcesEcsClusterD9504452
              - Arn
        - Action:
            - ecs:UpdateContainerInstancesState
            - ecs:ListTasks
          Condition:
            ArnEquals:
              ecs:cluster:
                Fn::GetAtt:
                  - EcsResourcesEcsClusterD9504452
                  - Arn
          Effect: Allow
          Resource: "*"
      Version: "2012-10-17"
    PolicyName: EcsResourcesAutoScalingGroupDrainECSHookFunctionServiceRoleDefaultPolicy039D81DC
    Roles:
      - Ref: EcsResourcesAutoScalingGroupDrainECSHookFunctionServiceRoleF2B1D493
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/DrainECSHook/Function/ServiceRole/DefaultPolicy/Resource
EcsResourcesAutoScalingGroupDrainECSHookFunction36970FB1:
  Type: AWS::Lambda::Function
  Properties:
    Code:
      ZipFile: >
        import boto3, json, os, time


        ecs = boto3.client('ecs')

        autoscaling = boto3.client('autoscaling')



        def lambda_handler(event, context):
          print(json.dumps(event))
          cluster = os.environ['CLUSTER']
          snsTopicArn = event['Records'][0]['Sns']['TopicArn']
          lifecycle_event = json.loads(event['Records'][0]['Sns']['Message'])
          instance_id = lifecycle_event.get('EC2InstanceId')
          if not instance_id:
            print('Got event without EC2InstanceId: %s', json.dumps(event))
            return

          instance_arn = container_instance_arn(cluster, instance_id)
          print('Instance %s has container instance ARN %s' % (lifecycle_event['EC2InstanceId'], instance_arn))

          if not instance_arn:
            return

          while has_tasks(cluster, instance_arn):
            time.sleep(10)

          try:
            print('Terminating instance %s' % instance_id)
            autoscaling.complete_lifecycle_action(
                LifecycleActionResult='CONTINUE',
                **pick(lifecycle_event, 'LifecycleHookName', 'LifecycleActionToken', 'AutoScalingGroupName'))
          except Exception as e:
            # Lifecycle action may have already completed.
            print(str(e))


        def container_instance_arn(cluster, instance_id):
          """Turn an instance ID into a container instance ARN."""
          arns = ecs.list_container_instances(cluster=cluster, filter='ec2InstanceId==' + instance_id)['containerInstanceArns']
          if not arns:
            return None
          return arns[0]


        def has_tasks(cluster, instance_arn):
          """Return True if the instance is running tasks for the given cluster."""
          instances = ecs.describe_container_instances(cluster=cluster, containerInstances=[instance_arn])['containerInstances']
          if not instances:
            return False
          instance = instances[0]

          if instance['status'] == 'ACTIVE':
            # Start draining, then try again later
            set_container_instance_to_draining(cluster, instance_arn)
            return True

          tasks = instance['runningTasksCount'] + instance['pendingTasksCount']
          print('Instance %s has %s tasks' % (instance_arn, tasks))

          return tasks > 0


        def set_container_instance_to_draining(cluster, instance_arn):
          ecs.update_container_instances_state(
              cluster=cluster,
              containerInstances=[instance_arn], status='DRAINING')


        def pick(dct, *keys):
          """Pick a subset of a dict."""
          return {k: v for k, v in dct.items() if k in keys}
    Handler: index.lambda_handler
    Role:
      Fn::GetAtt:
        - EcsResourcesAutoScalingGroupDrainECSHookFunctionServiceRoleF2B1D493
        - Arn
    Runtime: python3.6
    Environment:
      Variables:
        CLUSTER:
          Ref: EcsResourcesEcsClusterD9504452
    Tags:
      - Key: Name
        Value: awscdk/EcsResources/AutoScalingGroup
    Timeout: 310
  DependsOn:
    - EcsResourcesAutoScalingGroupDrainECSHookFunctionServiceRoleDefaultPolicy039D81DC
    - EcsResourcesAutoScalingGroupDrainECSHookFunctionServiceRoleF2B1D493
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/DrainECSHook/Function/Resource
? EcsResourcesAutoScalingGroupDrainECSHookFunctionAllowInvokeawscdkEcsResourcesAutoScalingGroupLifecycleHookDrainHookTopic831D8C0C71B13E09
: Type: AWS::Lambda::Permission
  Properties:
    Action: lambda:InvokeFunction
    FunctionName:
      Fn::GetAtt:
        - EcsResourcesAutoScalingGroupDrainECSHookFunction36970FB1
        - Arn
    Principal: sns.amazonaws.com
    SourceArn:
      Ref: EcsResourcesAutoScalingGroupLifecycleHookDrainHookTopic8C43F0F5
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/DrainECSHook/Function/AllowInvoke:awscdkEcsResourcesAutoScalingGroupLifecycleHookDrainHookTopic831D8C0C
EcsResourcesAutoScalingGroupDrainECSHookFunctionTopic1749A7BE:
  Type: AWS::SNS::Subscription
  Properties:
    Protocol: lambda
    TopicArn:
      Ref: EcsResourcesAutoScalingGroupLifecycleHookDrainHookTopic8C43F0F5
    Endpoint:
      Fn::GetAtt:
        - EcsResourcesAutoScalingGroupDrainECSHookFunction36970FB1
        - Arn
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/DrainECSHook/Function/Topic/Resource
EcsResourcesAutoScalingGroupLifecycleHookDrainHookRoleBFF8F321:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Statement:
        - Action: sts:AssumeRole
          Effect: Allow
          Principal:
            Service: autoscaling.amazonaws.com
      Version: "2012-10-17"
    Tags:
      - Key: Name
        Value: awscdk/EcsResources/AutoScalingGroup
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/LifecycleHookDrainHook/Role/Resource
EcsResourcesAutoScalingGroupLifecycleHookDrainHookRoleDefaultPolicy536AF9B8:
  Type: AWS::IAM::Policy
  Properties:
    PolicyDocument:
      Statement:
        - Action: sns:Publish
          Effect: Allow
          Resource:
            Ref: EcsResourcesAutoScalingGroupLifecycleHookDrainHookTopic8C43F0F5
      Version: "2012-10-17"
    PolicyName: EcsResourcesAutoScalingGroupLifecycleHookDrainHookRoleDefaultPolicy536AF9B8
    Roles:
      - Ref: EcsResourcesAutoScalingGroupLifecycleHookDrainHookRoleBFF8F321
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/LifecycleHookDrainHook/Role/DefaultPolicy/Resource
EcsResourcesAutoScalingGroupLifecycleHookDrainHookTopic8C43F0F5:
  Type: AWS::SNS::Topic
  Properties:
    Tags:
      - Key: Name
        Value: awscdk/EcsResources/AutoScalingGroup
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/LifecycleHookDrainHook/Topic/Resource
EcsResourcesAutoScalingGroupLifecycleHookDrainHookB4F4ED3D:
  Type: AWS::AutoScaling::LifecycleHook
  Properties:
    AutoScalingGroupName:
      Ref: EcsResourcesAutoScalingGroupASG32373EB9
    LifecycleTransition: autoscaling:EC2_INSTANCE_TERMINATING
    DefaultResult: CONTINUE
    HeartbeatTimeout: 300
    NotificationTargetARN:
      Ref: EcsResourcesAutoScalingGroupLifecycleHookDrainHookTopic8C43F0F5
    RoleARN:
      Fn::GetAtt:
        - EcsResourcesAutoScalingGroupLifecycleHookDrainHookRoleBFF8F321
        - Arn
  DependsOn:
    - EcsResourcesAutoScalingGroupLifecycleHookDrainHookRoleDefaultPolicy536AF9B8
    - EcsResourcesAutoScalingGroupLifecycleHookDrainHookRoleBFF8F321
  Metadata:
    aws:cdk:path: awscdk/EcsResources/AutoScalingGroup/LifecycleHookDrainHook/Resource
```
