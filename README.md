## Local Development

Build the backend container with:

```bash
docker build -t briancaffey.com:latest .
```

Run the backend container with:

```bash
docker run -it -v /home/brian/gitlab/briancaffey.com/backend/:/code briancaffey
.com:latest /bin/bash
```

## CloudFormation Commands

### sync templates to S3 bucket

Creating and updating stacks requires a template that is located in an S3 bucket. We provide the bucket URL in the `create-stack` and `update-stack` commands with the `--template-url` option.

```bash
aws s3 sync . s3://briancaffey.com-cloudformation/
```

### validate-template

The following command can be used to validate CloudFormation templates locally:

```bash
aws cloudformation validate-template --template-body file:///home/brian/gitlab/briancaffey.com/cloudformation/master.yaml
```

The above command will have this output:

```json
{
    "Description": "\nThis template deploys a VPC, with a pair of public and private subnets spread across two Availabilty Zones. It deploys an Internet Gateway, with a default route on the public subnets. It deploys a pair of NAT Gateways (one in each AZ), and default routes for them in the private subnets.\nIt then deploys a highly available ECS cluster using an AutoScaling Group, with ECS hosts distributed across multiple Availability Zones.\nFinally, it deploys a pair of example ECS services from co
    ntainers published in Amazon EC2 Container Registry(Amazon ECR).\nLast Modified: 22n d September 2016 Author: Paul Maddox < pmad
    dox @amazon.com > \n ",
    "CapabilitiesReason": "The following resource(s) require capabilities: [AWS::CloudFormation::Stack]",
    "Parameters": [],
    "Capabilities": [
        "CAPABILITY_NAMED_IAM",
        "CAPABILITY_AUTO_EXPAND"
    ]
}
```

### create-stack

```bash
aws cloudformation create-stack --stack-name briancaffey --template-url https://s3.amazonaws.com/briancaffey.com-cloudformation/master.yaml --capabilities=CAPABILITY_NAMED_IAM
```

### update-stack

```bash
aws cloudformation update-stack --stack-name briancaffey --template-url https://s3.amazonaws.com/briancaffey.com-cloudformation/master.yaml --capabilities=CAPABILITY_NAMED_IAM
```
