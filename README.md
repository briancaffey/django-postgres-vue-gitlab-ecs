## Project Documentation

Documentation for this project can be found here:

[https://verbose-equals-true.gitlab.io/django-postgres-vue-gitlab-ecs/](https://verbose-equals-true.gitlab.io/django-postgres-vue-gitlab-ecs/)


## Project Architecture Overview

Here is an overview of the project architecture, including the CI/CD pipeline and the AWS infrastructure that will be automatically provisioned through the AWS Cloud Development Kit:

![png](/architecture.png)

(This diagram was created with [draw.io](https://draw.io). Here's the link to the a read-only version of the diagram on draw.io: [https://drive.google.com/file/d/1gU61zjoW80fCusUcswU1zhEE5VFB1Z5U/view?usp=sharing](https://drive.google.com/file/d/1gU61zjoW80fCusUcswU1zhEE5VFB1Z5U/view?usp=sharing)

### Legend

1 - GitLab is used to host the source code, test the source code and deploy the application to AWS.

2 - Unit testing (see `.gitlab-ci.yml`)

2a - Pytest

2b - Jest

2c - Cypress

3 - Deployment phase (see `/gitlab-ci/aws/cdk.yml`)

3a - Quasar PWA assets are built if there are changes in the `quasar` directory

3b - AWS Cloud Development Kit (CDK) defines all infrastructure in AWS (4a - 12)

3c - AWS CLI is used to run Fargate tasks through manual GitLab CI jobs

4 - CDK Assets (ECR and S3 buckets that CDK uses internally to manage build assets and artifacts)

4a - Elastic Container Repository is used to manage the Django docker image used in various parts of the application

4b - S3 bucket used to store files associated with CDK and CloudFormation

5 - Route53 is used to route traffic to the CloudFront distribution

6 - CloudFront distribution that serves as the "front desk" of the application. It routes requests to to the correct CloudFront Origin

7 - CloudFront Origin Configurations

7a - S3 bucket for Quasar PWA assets

7b - Application Load Balancer for Django application (`/api/`, `/admin/`, `/flower/`, `/ws/`, `/graphql/`)

7c - S3 bucket for Django assets (static files, public media and private media)

8 - Web server and websocket servers

8a - Fargate service running uvicorn process (REST, GraphQL, Django Channels)

8b - Autoscaling Group for Fargate Service that serves Django API

9 - Celery and celery worker autoscaling

9a - Fargate service that is autoscaled between 0 and `N` Fargate tasks for a given celery queue

9b - Scheduled Event that triggers a Lambda to make a request to Django backend which collects celery queue metrics and published metrics to CloudWatch using boto3

9c - Lambda event the makes a request to `/api/celery-metrics/`

9d - CloudWatch alarm that is used to scale the Fargate service for a celery queue

9e - Autoscaling group for celery Fargate service

10 - Fargate tasks that run Django management commands such as `migrate` and `collectstatic`. These are triggered from manual GitLab CI jobs using the AWS CLI (3c)

11 - ElastiCache for Redis, used for Caching, Celery Broker, Channels Layer, etc.

12 - Aurora Postgres Serverless

## Local Development

First, copy `.env.template` to a new file in the project's root directory called `.env`. This file will be read by `docker-compose` in the next step. Adjust any of the values in this file if needed, or add new variables for any secret information you need to pass to docker-compose (or to docker containers).

```sh
docker-compose up
```

Open `http://localhost` in your browser.

You can specify environment variables for docker-compose by adding an `.env` file to the root of the project based on `.env.template`.

### Social Authentication Keys

To use social sign on in local development, you will need to create an application with the given provider such as GitHub, Google, Facebook, etc.

#### GitHub

Go to [https://github.com/settings/applications/new](https://github.com/settings/applications/new), and add the following:

- Application Name: A name for the development application, such as `My App Dev`
- Homepage URL: `http://localhost`
- Application description: (optional)
- Authorization callback URL `http://localhost/auth/github/callback` (this route is defined in `quasar/src/router/routes.js`)

In the `.env` file, add the `Client ID` of your GitHub OAuth App as the `GITHUB_KEY` variable, and add the `Client Secret` as the `GITHUB_SECRET` variable.

## VuePress Documentation

This project uses VuePress for documentation. To view the documentation site locally, run the following command:

```bash
docker-compose -f compose/docs.yml up --build
```

This will make the docs available at `http://localhost:8082/docs/`. Hot-reloading through websockets is supported, so changes will show up as they are saved in your code editor.

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
