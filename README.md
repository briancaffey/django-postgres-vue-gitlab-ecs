## Project Documentation

Documentation for this project can be found here:

[https://verbose-equals-true.gitlab.io/django-postgres-vue-gitlab-ecs/](https://verbose-equals-true.gitlab.io/django-postgres-vue-gitlab-ecs/)

## Architecture

![png](/architecture.png)

## Local Development

First, copy `.env.template` to a new file in the project's root directory called `.env`. This file will be read by `docker-compose` in the next step. Adjust any of the values in this file if needed, or add new variables for any secret information you need to pass to docker-compose (or to docker containers).

## Current Project Goals

Currently I am working on replacing CloudFormation with CDK for infrastructure and deployment.

To work with CDK, do the following:

- Make sure you are using at least version 10 of node: `nvm use 13`
- Activate the virtual environment with `source awscdk/.env/bin/activate`
- `pip install -e awscdk` to install CDK dependencies

### Social Authentication Keys

To use social sign on in development, you will need to create an application with the given provider.

#### GitHub

Go to [https://github.com/settings/applications/new](https://github.com/settings/applications/new), and add the following:

- Application Name: A name for the development application, such as `My App Dev`
- Homepage URL: `http://localhost`
- Application description: (optional)
- Authorization callback URL `http://localhost/auth/github/callback` (this route is defined in `quasar/src/router/routes.js`)

In the `.env` file, add the `Client ID` of your GitHub OAuth App as the `GITHUB_KEY` variable, and add the `Client Secret` as the `GITHUB_SECRET` variable.

```sh
docker-compose up --build
```

Open `http://localhost` in your browser.

You can specify environment variables for docker-compose by adding an `.env` file to the root of the project based on `.env.template`.

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

# Running tests

This project uses Pytest, Jest and Cypress for testing. This section describes the different ways to run tests locally.

To run Pytest and Jest, you can use `docker-compose exec`, or you can shell into the container.

Using `docker-compose exec`:

```
docker-compose exec backend pytest
```

```
docker exec -it backend bash
root@b24c4206002e:/code# pytest
```

To run Jest tests, you can run:

```
docker-compose exec frontend npm run test
```

## Integration tests

Cypress can be used in an interactive mode with a UI, or it can be used in a headless way (such as in GitLab CI).

## Running Cypress Interactively

To run Cypress tests interactively, install Cypress in the root of the project:

```
npm install cypress
```

Then open Cypress with:

```
$(npm bin)/cypress open --config baseUrl=http://localhost
```

Click on the button "Run all specs", and the tests will start running in a new browser window with a log of Cypress actions and test statements displayed on the left side.

## Run Cypress in headless mode

There are two ways to run Cypress in headless mode. You can run Cypress against the `docker-compose` file in `compose/test.yml`, or you can run the Cypress test using `gitlab-runner`.

### Using `compose/test.yml`

To run the test locally against the production image, run the following:

```
docker-compose -f compose/test.yml up --build
```

This will build a special environment that resembles the environment used in GitLab CI. It brings up three containers: redis, postgres and backend. The backend serves several purposes: it runs the Django webserver, it runs the ASGI server used by Django Channels, and it runs celery tasks synchronously, and it also serves the Vue application through Django templates and static files. See the Dockerfile located at `backend/scripts/prod/Dockerfile` for details on how this works.

Make sure that Cypress is properly installed with:

```
$(npm bin)/cypress verify
```

Then start the tests with:

```
$(npm bin)/cypress run --config baseUrl=http://localhost:9000
```

You could also run these tests in the interactive mode using `compose/test.yml` with the following command:

```
$(npm bin)/cypress open --config baseUrl=http://localhost:9000
```

Note that this is similar to the previous command, but we are using the `open` command instead of the `run` command.

### Using `gitlab-runner`

It can be useful to debug your `.gitlab-ci.yml` jobs before pushing changes to GitLab. This gives us a faster feedback loop, and it doesn't use any of the CI minutes on your free (2000 minutes/month) or paid GitLab plans.

There is a little bit of setup needed to run Cypress tests with `gitlab-runner`.

First, you need to install `gitlab-runner` on your machine.

Next, you need to start a local registry on you r computer. Run the following command ([taken from docker documentation](https://docs.docker.com/registry/deploying/)):

```
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

Next, you need to build the production image that you will use in the test. To do this, run the following command:

```
docker-compose -f compose/test.yml build backend
```

Then tag the image with the following command:

```
docker tag compose_backend:latest localhost:5000/backend:latest
```

Then push the tagged image to the local registry:

```
docker push localhost:5000/backend:latest
```

Now that we have pushed the production image to our local registry, we can run the `e2e-local` job with `gitlab-runner`.

To do this, we need to make sure that the `e2e-local` job defined in `.gitlab-ci.yml` is not commented. To do this, remove the `.` in front of the job name (change `.e2e-local` to `e2e-local`).

Then, commit your changes in git. Gitlab runner requires that you commit changes before running tests. Run the GitLab CI job with the following command:

```
gitlab-runner exec docker e2e-local
```

Before you push your changes to GitLab, make sure that you uncomment the `e2e-local` job by adding `.` in front of it (`.e2e-local`).

# ToDo

- Add diagram of local development
- Put django apps in apps folder
- Redeploy django app to check settings files
- Add GitLab pages site for Group project
- Add file upload examples with Django REST Framework
- Setup password reset
