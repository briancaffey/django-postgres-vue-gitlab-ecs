# Deploying on AWS

This guide provides an overview of how to deploy the project on AWS using CloudFormation, the AWS CLI and GitLab CI. CloudFormation allows us to define all of our AWS resources in YAML files called CloudFormation templates. GitLab CI will be used to automate the AWS commands used to update the project in production.

## GitLab CI

GitLab CI is defined by the `gitlab-ci.yml` file in the root directory of the project repository. This YAML is composed of multiple `stages`. Each stage is composed of one or more `jobs`. The `gitlab-ci.yml` file imports another file with the `include` keyword. This merges `gitlab-ci.yml` with the files listed in `include`, such as `/gitlab-ci/aws.yml`. The jobs in a given stage all run in parallel. If one of the jobs in a stage fails, the entire pipeline is stopped and jobs from the following stages are not carried out. Here are the current stages of the project's GitLab CI:

- documentation
- test
- build
- integration
- release
- deploy

### Documentation

`documentation` builds the project documentation site using GitLab Pages and publishes it to this address: [https://verbose-equals-true.gitlab.io/django-postgres-vue-gitlab-ecs/](https://verbose-equals-true.gitlab.io/django-postgres-vue-gitlab-ecs/).

### Test

`test` runs unit tests in Python and Javascript. These tests are run in parallel.

### Build

`build` builds the static frontend site as well as the backend docker image. These jobs also run in parallel. The backend docker image uses a multi-stage build that consist of three stages: `build-stage`, `production` and `gitlab-ci`. The build stage builds the frontend assets that are used in the integration tests (the following stage). The `production` stage produces an image that is used in production (it is sent to ECR, the AWS image repository, in the `release` stage), and the `gitlab-ci` stage prepares an image that contains the Django application that serves the frontend site from static files. This is done to simplify the integration testing (this will be covered in depth in another section). The production docker image is then sent to the private GitLab container repository attached to our GitLab account. This image is accessed in the `release` stage.

### Integration

`integration` runs integration tests. This tests simulates actions that users would take in the actual application. It uses Cypress, a testing library. We can also run python commands to seed our test database with data that will be used in the tests, such as users that we can use to login with in the tests. The integration tests are recorded and saved as `.mp4` files that be viewed in GitLab. This gives us another way to check that the test are doing what we expect them to be doing, and viewing the videos along with the test job logs can be useful in debugging failing tests.

### Release

`release` releases the backend image from the GitLab container registry to the AWS container registry once it has passed integration tests.

### Deploy

`deploy` contains several jobs. It takes the build files for the static frontend site (that were generated in the `build` stage) and sends them the S3 bucket that serves our site using a CloudFront distribution (CDN). The deploy stage also updates the CloudFormation stack. This will make any infrastructure changes in our CloudFormation templates. In general, the only change that will be made to the CloudFormation stack is an updated container image. This causes the ECS services to update to newer versions. The `deploy` stage has two additional stages that are *manual*: `migrate` and `collectstatic`. Manual stages are triggered from the GitLab UI. These jobs run database migrations and run the Django command `collectstatic` that moves static files to the S3 bucket that serves static files. We don't have many static files in this project, but the Django admin and the Django REST Framework both have static files that need to be served in production. Finally, GitLab pages will create a `deploy` job when it publushes a new version of the documentation site.

## CloudFormation

CloudFormation is an Infrastructure as Code (IaC) service from Amazon. This section will discuss how CloudFormation is used in the project. All of the the CloudFormation templates are defined in the `/cloudformation` directory in the root of the project.

Here is the directory structure of the `cloudformation` folder:

```
cloudformation
├── infrastructure
│   ├── django-assets.yaml
│   ├── ecr-repository.yaml
│   ├── ecs-cluster.yaml
│   ├── elasticache-redis.yaml
│   ├── load-balancers.yaml
│   ├── rds-postgres.yaml
│   ├── service-role.yaml
│   ├── static-site.yaml
│   └── vpc.yaml
├── master.yaml
├── scripts
│   └── generate_secrets.py
├── services
│   ├── backend.yaml
│   ├── beat.yaml
│   ├── celery.yaml
│   ├── daphne.yaml
│   └── flower.yaml
├── tasks
│   ├── collectstatic.yaml
│   └── migrate.yaml
└── tests
    └── validate-templates.sh
```

### `master.yml`

`master.yml` is the template that references all of the resources in our AWS infrastucture as *nested stacks*. This helps keep files small, but there would be nothing wrong with defining all of our cloud resources in one big file. Notice that all of the `Resources` defined in `master.yml` are of `Type: AWS::CloudFormation::Stack` that each have a unique `TemplateURL`. Also, notice the `Parameters` section of `master.yml`. These values are specific to our application: URL names, passwords, SSL certificates, etc. These values come from GitLab CI.

Let's go back to the `Create stack` job located in `/gitlab-ci/aws.yml`. Here's the job definition:

```yml
.Create stack:
  image: python:3.7
  stage: deploy
  variables:
    EnvironmentName: staging
  before_script:
    - pip install awscli
    - ./cloudformation/tests/validate-templates.sh
    - ./cloudformation/scripts/generate_secrets.py
    - aws s3 sync cloudformation/ s3://${AppUrl}-cloudformation/ --delete
  script:
    - |
      aws cloudformation create-stack \
        --stack-name ${StackName} \
        --template-url https://s3.amazonaws.com/${AppUrl}-cloudformation/master.yaml \
        --capabilities=CAPABILITY_NAMED_IAM \
        --parameters file://./parameters.json
  after_script:
    - echo "Create stack complete"
```

In the `before_script` section, we install the aws cli for use in the `script` section, and we run a script to validate our CloudFormation templates and another script that extracts environment values from the environment into a file called `parametes.json` that is also used in the `script` section.

In the `script` section, we call the `aws cloudformation create-stack` command. We pass parameters including the stack name, the URL of the S3 bucket where the template is stored (`master.yaml`), an acknowledgement that the command will create resources for us (`--capabilities`), and also the parameters that are passed to the `master.yaml` template.

Notice that `/gitlab-ci/aws.yml` has two similar jobs: `Create stack` and `Update stack`. `Create stack` is run once, and then it is *commented* by placing a `.` in front of the job name (`.Create stack`). This will prevent the job from running in future deployments. Instead, we will update the CloudFormation stack with the `Update stack` job. Initially, this job is commented, but we uncomment it once the stack has been created, so the next time we push to the master branch the existing stack is updated.

### Infrastructure

The `infrastructure` template contains most of the core pieces of infrastructure in our cloud deployment. Here's a description of each nested infrastructure stack with a few important things to note about each stack:

- `django-assets.yaml`

This template deploys S3 buckets for serving Django static files. This is the bucket that we will send files to when we run the `collectstatic` manual job in GitLab CI.

- `ecr-repository.yaml`

This stack deploys an Elastic Container Repository that the `release` stage deploys the production docker image to in GitLab CI. We need to run the `Create stack` job before we run the `Release backend` job since the `Release backend` job relies on the ECR Repository created in this stack.

- `ecs-cluster.yaml`

This stack contains the ECS Cluster and a number of supporting resources such as Roles, an autoscaling group and a launch configuration for our container instances (EC2 instances in our ECS cluster).

- `elasticache-redis.yaml`

This stack brings up an ElastiCache instance that will run our single-node redis cluster. This is required for caching, celery, and Django Channels.

- `load-balancers.yaml`

This stack includes resources related to load balancing, including security groups, ingresses, listeners, and record sets for subdomains that will be serve as the endpoint URLs for the services in our ECS cluster.

- `rds-postgres.yaml`

This stack brings up a managed relational database running PostgreSQL

- `service-role.yaml`

This stack configures an IAM role that grants the services access to register/unregister with the Application Load Balancer (ALB). Notice that this resource is referenced several times in our `master.yaml` stack by different ECS services.

- `static-site.yaml`

This stack brings up resources that support our frontend site: and S3 bucket, a CloudFront distribution, and DNS record sets. This stack can take up to 30 minutes to deploy because the CloudFront distribution takes time to setup a global CDN across the AWS network.

### Services

The `services` folder contains templates for nested stacks that represent ECS services. An ECS **service** is responsible for running a certain number of a **task**, and also specifies load balancing. A **task** defines which container to run with a `ContainerDefinition`, along with environment variables and resource limits, port mapping, and logging information.

Not all services require load balancing. The `backend`, `daphne` and `flower` containers have load balancing because they need to be able to handle HTTP requests. The `celery` and `beat` containers run in the background and do not need to respond to HTTP requests. Rather, the `celery` task processes tasks from the task queue, and the `beat` service schedules tasks defined as cron jobs in our Django application.

Notice that the different containers have different `command`s, which are the processes that the containers will run when started.

### Tasks

As mentioned earlier, we have two manual jobs in our GitLab CI pipeline. These are the `migrate` and `collectstatic` tasks that are run once, and then don't run again once they have completed. These tasks are not wrapped by services, because services help keep tasks running indefinitely, and we don't need to keep these one-off processes running once they have exited.

### Scripts

There is one script in our `scripts` folder, and this script generates a file that contains parameters that are passed to the `Create stack` and `Update stack` commands.

### Tests

The `tests` folder contains one test which validates the CloudFormation templates. This can help prevent CloudFormation from having to rollback deployments because of syntax errors or other problems in our YAML templates.

