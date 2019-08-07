# NGINX

At this point it makes sense to introduce NGINX.

NGINX is a webserver and reverse proxy that will play an important role in our application. NGINX is analogous to the "front desk" in our applicatoin in that it directs traffic to the files or service URLs that we specify.

For example, we will tell NGINX to send all requests that start with `/api` or `/admin` to be sent to our Django container, not our `node` server. This makes sense, because our `node` server won't know what to do with `/api` or `/admin` requests.

## Docker Compose Configuration

If you are familiar with Django's URL routing, I think it is fair to say that NGINX is like a higher-level version of `urls.py` in that it directs traffic based on the properties of the incoming URLs. It will also handle `https`, serving static files, and more. We'll see all of this later, but for now let's just introduce it to our `docker-compose.dev.yml` file so we can use it in local development.

Let's add the following to our `docker-compose.dev.yml` file:

```yml
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - backend
    volumes:
      - ./nginx/dev.conf:/etc/nginx/nginx.conf:ro
    networks:
      - main
```

We don't need a `Dockerfile` for this service since we only need the base image: `nginx:alpine`. This means that we don't need to specify a `build` section for the service definition.

## NGINX Configuration

Note that we do need to mount a file called `dev.conf` into the container. This will be the NGINX configuration file that we write to tell NGINX how to handle traffic that it receives on port `80`.

Let's make a top-level folder called `nginx`, and inside that folder create a file called `dev.conf` with the following content:

**nginx/dev.conf**

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

  upstream frontend {
    server frontend:8080;
  }

  server {
    listen 80;
    charset utf-8;

    # frontend urls
    location / {
    proxy_redirect off;
    proxy_pass http://frontend;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $http_host;
    }

    # frontend dev-server
    location /sockjs-node {
      proxy_redirect off;
      proxy_pass http://frontend;
      proxy_set_header X-Real-IP  $remote_addr;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header Host $host;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
    }

    # backend urls
    location ~ ^/(admin|api|static) {
      proxy_redirect off;
      proxy_pass http://backend;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $http_host;
    }
  }
}
```

Now visit `localhost` and you should see the Vue app as well as some logs from the `nginx` service in the docker-compose output with `200` status messages. Remeber, visiting `localhost` in your browser is equivalent to visiting `localhost:80`.

`localhost/admin` should display the Django admin interface.

You might have some other service running on your local machine that is using port 80. If we tried to map port `80` on our host to port `80` in a container while port `80` on our host was in use, the docker engine would tell us that the service is not available and it would not start the container.

Let's commit these changes and then make some additional optimizations.

```
git add .
git commit -m "added nginx service and added configuration file to new nginx directory"
```

### Serve Django Static Files from NGINX

One simple optimization we can make is not serving static files from Django. By using a shared volume, we can add Django's static files to the NGINX file system so that it can serve resources directly from it's own container. (Later on we will use a similar technique for adding our production-ready VueJS application to NGINX).

We need to change the following files to do this:

1. Edit `docker-compose.dev.yml`
2. Move `nginx/dev.conf` to `nginx/dev/dev.conf`
3. Edit `nginx/dev/dev.conf`
4. Add `nginx/dev/DockerfileDev`

In `docker-compose.dev.yml`, we will need to do the following:

- Add a `django-static` volume:

```yml
volumes:
  django-static:
```

- Change the `build` section of the `backend` container:

```yml
    build:
      context: .
      dockerfile: nginx/dev/Dockerfile
```

- Mount `django-static` in the `backend` container:

```yml
    volumes:
      - .:/code
      - django-static:/backend/static
```

- Mount `django-static` in the `nginx` container:

```yml
    volumes:
      - ./nginx/dev/dev.conf:/etc/nginx/nginx.conf:ro
      - django-static:/usr/src/app/static
```

In `nginx/dev/dev.conf` we need to do the following:

- remove `static` from the `location ~ ^/(admin|api|static)` location block
- create a new `static` block right after the `(admin|api)` location block as follows:

```
    # static files
    location /static {
      autoindex on;
      alias /usr/src/app/static;
    }
```

Finally, add `nginx/dev/Dockerfile`:

```
FROM nginx:1.13.12-alpine
COPY nginx/dev/dev.conf /etc/nginx/nginx.conf
COPY backend/static /usr/src/app/static/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

When we restart docker-compose, we should now see that our static files are served from NGINX directly.

Let's commit our changes:

```
git add .
git commit -m "optimized Django application by serving static files from nginx"
```
