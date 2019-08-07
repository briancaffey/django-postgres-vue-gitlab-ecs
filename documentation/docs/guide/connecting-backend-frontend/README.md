# Connecting our backend and frontend

Let's get our backend talking to our frontend. We want to make API calls from our VueJS application that will return data from our Django backend.

Let's keep this as simple as possible and simply list the `Post` objects on the front page of our VueJS application right under the VueJS logo. Also, let's remove the `HelloWorld.vue` component.

To do this, we only need to add the following to the `Home.vue` file:

1. a `fetchPosts` method in the `methods` section of the `script` part of the sigle-file component.

2. a `mounted` method that calls `this.fetchPosts` to load the posts when the component is mounted.

3. `data()` method that will return an object that holds `posts: []`

4. String interpolation in the `template` that will display the `title` and `content` attributes of our posts.

Here's what my `Home.vue` file looks like:

**frontend/src/views/Home.vue**

```html
<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <h3>Posts</h3>
    <div v-for="(post, i) in posts" :key="i">
      <h4>{{ post.title }}</h4>
      <p>{{ post.content }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
  data() {
    return {
      posts: [],
    };
  },
  mounted() {
    this.fetchPosts();
  },
  methods: {
    fetchPosts() {
      fetch('/api/posts/', {
        method: 'GET',
        headers: {
          Accept: 'application/json',
        },
      })
        .then((response) => {
          if (response.ok) {
            response.json().then((json) => {
              this.posts = json;
            });
          }
        });
    },
  },
};
</script>
```

Let's go back to our `REST_FRAMEWORK` settings in `settings.py` and comment out the following line:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}
```

Now when we load the Vue app, we should see an error in the developer console saying:

```
GET http://localhost:8001/api/posts/ 401 (Unauthorized)
```

This means that our request is getting to the backend, but since we are not passing a JWT with the header of the request and we are not logged in with session authentication, we are getting a `401 Unauthorized` status code.

We want to be able to


Let's override the default settings by changing the `PostList` view:

**backend/posts/views.py**

```python
from rest_framework.decorators import (
    authentication_classes,
    permission_classes
)

...

class PostList(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

When we save `views.py`, we should see the posts displayed in the VueJS app. Let's remove these changes from `views.py` as they would break our tests.

We can keep the changes to `REST_FRAMEWORK`. This will leave an important task for us to handle later: adding authentication to our VueJS applicatoin. Let's commit these changes.

```
git add .
git commit -m "added an api call to frontend VueJS app to list posts"
```

## Production Environment

So far we have been working on our `docker-compose.dev.yml` file that we will use for local development of our application. Let's revisit `docker-compose.yml`. This file will be used t build our production environment. Let's create a new branch called `feature-prod` where we will make changes for our production environment. Let's also merge our current branch, `feature-vue` and create a new minor release.

```
git add .
git commit -m "updated readme"
git checkout develop
git merge feature-vue
git checkout -b release-0.0.3
git checkout master
git merge release-0.0.3 --no-ff
git tag -a 0.0.3
git push --all
git push --tags
```

## Production Environment

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

### `nginx`

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

Now let's look at `nging/prod/Dockerfile`:

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
