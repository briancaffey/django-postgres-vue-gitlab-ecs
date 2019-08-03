## Architecture

![png](/architecture.png)

## Local Development

First, copy `.env.template` to a new file in the project's root directory called `.env`. This file will be read by `docker-compose` in the next step. Adjust any of the values in this file if needed, or add new variables for any secret information you need to pass to docker-compose (or to docker containers).

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

# Current Issues

Currently Cypress tests are passing locally, but some of the test are failing in GitLab CI.

To run Cypress locally you can either run Cypress directly on your computer against the containerized application (for active development), or you can run Cypress in a container against the containerized application (this should be the same environment in GitLab CI using docker-compose with dind).

To setup Cypress locally, run:

```
npm install cypress --save
```

Then open Cypress with:

```
$(npm bin)/cypress open
```

Run cypress tests locally by running the following commands. First build the application stack and cypress container:

```
docker-compose -f docker-compose.ci.yml -f cypress.yml build
```

Then start the application:

```
docker-compose -f docker-compose.ci.yml up -d
```

Then run cypress tests:

```
docker-compose -f docker-compose.ci.yml -f cypress.yml up
```

# ToDo

- Fix Cypress testing in GitLab CI
- Add diagram of local development
- Put django apps in apps folder
- Redeploy django app to check settings files
- Add GitLab pages site for Group project
- Decide how to build the documentation site (quasar, vuepress?)
- Add file upload examples with Django REST Framework
- Setup password reset
