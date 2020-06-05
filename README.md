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
- run `cdk synth --app awscdk/app.py --output awscdk/cdk.out` and view the resulting JSON for the nested CloudFormation stacks in `awscdk/cdk.out`

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

# ToDo

- Add diagram of local development
- Put django apps in apps folder
- Redeploy django app to check settings files
- Add GitLab pages site for Group project
- Add file upload examples with Django REST Framework
- Setup password reset
