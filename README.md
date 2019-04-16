## Architecture

![png](/draw.png)

## Local Development

```
docker-compose up --build
```

Open `http://localhost` in your browser

You can specify environment variables for docker-compose by adding an `.env` file to the root of the project based on `.env.template`.

### Access Django Shell in Jupyter Notebook

With all containers running, run the following commands:

```
docker exec -it backend bash
# cd notebooks/
# ../manage.py shell_plus --notebook
```

or use this single command:

```
docker exec -it backend bash -c 'cd notebooks && ../manage.py shell_plus --notebook'
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

## Enable SSH Access to EC2 Instances with KeyPair

https://github.com/aws-samples/ecs-refarch-cloudformation/issues/62

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-keyname

Also, we need to update a security group rule to allow SSH connections on port 22.


## TODO

- Tear down the stack (click the button that says delete stack)
- Make sure that we have documented the changes to make in our template

- static site, ALB certificate, ECR Repo, Comment out the container definition until our stack is up and we have pushed the image to the ECR repo.



## Questions

Is it true that you can use either HostedZoneName or HostedZoneId but not both?