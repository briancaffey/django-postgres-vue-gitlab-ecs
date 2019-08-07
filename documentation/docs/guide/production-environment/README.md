# Production Environment

## Changes to make

Let's think about what we need to change in `docker-compose.dev.yml` for our production environment:

1. `nginx`
  - We need to create `prod.conf` to replace `dev.conf`
  - In `prod.conf`, we need to remove the `frontend` server since we won't be using `frontend` in production
  - In `prod.conf`, we want to serve our VueJS as static files.
  - We need to add a new `Dockerfile` that will use a multi-stage build to get the production-ready VueJS static files into the `nginx` container

2. `backend`
  - We will want to add `gunicorn`, a production-ready webserver that will replace the `runserver` command that we are using for development. We will split `start.sh` into `start_dev.sh` and `start_prod.sh`.
  - We also need to change the `Dockerfile` for backend to copy both `start_dev.sh` and `start_prod.sh`

3. `frontend`
  - We will remove this service for production.

### NGINX

Let's create a `prod` folder in `nginx` that will live next to `nginx/dev`. Create `prod.conf` in this folder:

**nginx/prod/prod.conf**

```
user  nginx;
worker_processes  1;

events {
  worker_connections  1024;
}

http {
  include /etc/nginx/mime.types;
  client_max_body_size 100m;

  upstream backend {
    server backend:8000;
  }

  server {
    listen 80;
    charset utf-8;

    root /dist/;
    index index.html;

    # frontend
    location / {
      try_files $uri $uri/ @rewrites;
    }

    location @rewrites {
      rewrite ^(.+)$ /index.html last;
    }

    # backend urls
    location ~ ^/(admin|api) {
      proxy_redirect off;
      proxy_pass http://backend;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $http_host;
    }

    # static files
    location /static {
      autoindex on;
      alias /usr/src/app/static;
    }
  }
}
```

Now let's look at `nginx/prod/Dockerfile`:

```
# build stage
FROM node:9.11.1-alpine as build-stage
WORKDIR /app/
COPY frontend/package.json /app/
RUN npm cache verify
RUN npm install
COPY frontend /app/
RUN npm run build

# production stage
FROM nginx:1.13.12-alpine as production-stage
COPY nginx/prod/prod.conf /etc/nginx/nginx.conf
COPY backend/static /usr/src/app/static/
COPY --from=build-stage /app/dist /dist/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

This uses a multi-stage build. In the build stage, we start with a `node` container that builds our static files for the VueJS application. Then, in the production stage, files from the `node` container are mounted into the `nginx` container that the production stage uses. A multi-stage build like this is the official recommendation for Dockerizing VueJS applications.

### Backend

For the `backend`, let's start with `requirements.txt`:

```python
...
gunicorn==19.8
...
```

Let's use `gunicorn` in `backend/scripts/stat_prod.sh`:

```sh
#!/bin/bash

cd backend
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate --no-input
gunicorn backend.wsgi -b 0.0.0.0:8000
```

Be sure to make this file executable, as well as `start_dev.sh`. Also, in `docker-compose.dev.yml`, change the `backend` command from `/start.sh` to `/start_dev.sh`.

Let's change the `backend` Dockerfile:

```
FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
COPY scripts/start*.sh /
ADD . /code/
```

We only changed `start.sh` to `start*.sh`. This will `COPY` both of our shell scripts used to start Django. This way we don't need two separate Dockerfiles for `backend`.

Let's test the environment by running:

```
docker-compose up --build
```

This seems to work fine: we can access both the VueJS app and the Django application's admin site.

Let's commit our changes.

```
git add .
git commit -m "completed basic production environment"
```

Now let's merge this branch and create a new minor release:

```
git add .
git commit -m "updated readme"
git checkout develop
git merge feature-prod
git checkout -b release-0.0.4
git checkout master
git merge release-0.0.4 --no-ff
git tag -a 0.0.4
git push --all
git push --tags
```
