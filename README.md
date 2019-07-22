## Architecture

![png](/architecture.png)

## Local Development

First, copy `.env.template` to a new file in the project's root directory called `.env`. This file will be read by `docker-compose` in the next step. Adjust any of the values in this file if needed, or add new variables for any secret information you need to pass to docker-compose (or to docker containers).

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

# ToDo

- Add diagram of local development
- Put django apps in apps folder
- Redeploy django app to check settings files
- Add GitLab pages site for Group project
- Decide how to build the documentation site (quasar, vuepress?)
- Add Cypress testing using simple setup with gitlab-ci.yml and services from private registry
- Add file upload examples with Django REST Framework
- Setup password reset
