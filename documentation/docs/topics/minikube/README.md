# Minikube

Minikube is a tool for running a single-node kubernetes cluster inside of a virtual machine. It is a popular tool for developing Kubernetes applications locally.

This topic will cover using `minikube` to set up the project Kubernetes locally.

I'll be following [this guide](https://medium.com/@markgituma/kubernetes-local-to-production-with-django-1-introduction-d73adc9ce4b4) to get started.

## Getting started

### Start minikube

To get started, bring up `minikube` with

```bash
minikube start
```

Optionally, run `minikube delete`, and then `minikube start` to start with a clean cluster.

I'll be using the following alias to use `kubectl`:

```bash
alias k='kubectl'
```

## Build the Django server Deployment

We need to build our `backend` image. In order for minikube to be able to use the image, we can set our docker client to point to the minikube docker host. To do this, run the following command:

```
eval $(minikube docker-env)
```

`$(minikube docker-env)` results in the following output:

```bash
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="/home/brian/.minikube/certs"
# Run this command to configure your shell:
# eval $(minikube docker-env)
```

Notice that the `DOCKER_HOST` is pointing to the minikube VM on docker's default port `2376`.

With these environment variables set, let's build the Django container image with the following command:

```bash
docker build -t backend:<TAG> -f backend/scripts/dev/Dockerfile backend/
```

**`deployment.yml`**

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-backend
  labels:
    app: django-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: django-backend
  template:
    metadata:
      labels:
        app: django-backend
    spec:
      containers:
        - name: django-backend-container
          image: localhost:5000/backend
          command: ["./manage.py", "runserver"]
          ports:
          - containerPort: 8000
```

Let's send this file to Kubernete API server with the following command:

```
kubectl apply -f kubernetes/django/deployment.yml
```

Your pod for the deployment should be starting. Inspect the pods with `k get pods`. If there is an error with container startup, you might see something like this:

```
k get pods
NAME                             READY   STATUS   RESTARTS   AGE
django-backend-dd798db99-hkv2p   0/1     Error    0          3s
```

If this is the case, inspect the logs of the container with the following command:

I have intentionally cause the container to fail by not providing a `SECRET_KEY` environment variable (this is something that Django needs in order to start).

Let's inspect the container logs to confirm this:

```bash
k logs django-backend-dd798db99-hkv2p
Traceback (most recent call last):
  File "./manage.py", line 16, in <module>
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/__init__.py", line 381, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python3.7/site-packages/django/core/management/__init__.py", line 375, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/base.py", line 323, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/commands/runserver.py", line 60, in execute
    super().execute(*args, **options)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/base.py", line 364, in execute
    output = self.handle(*args, **options)
  File "/usr/local/lib/python3.7/site-packages/django/core/management/commands/runserver.py", line 67, in handle
    if not settings.DEBUG and not settings.ALLOWED_HOSTS:
  File "/usr/local/lib/python3.7/site-packages/django/conf/__init__.py", line 79, in __getattr__
    self._setup(name)
  File "/usr/local/lib/python3.7/site-packages/django/conf/__init__.py", line 66, in _setup
    self._wrapped = Settings(settings_module)
  File "/usr/local/lib/python3.7/site-packages/django/conf/__init__.py", line 176, in __init__
    raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")
django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty.
```

We could either provide a fallback value in the Django settings (which would require rebuilding the image), or we could add an environment variable to the container definition in the Pod `spec` in `deployment.yml`:

```yml
    spec:
      containers:
        - name: backend
          imagePullPolicy: IfNotPresent
          image: backend:latest
          command: ["./manage.py", "runserver"]
          ports:
          - containerPort: 8000
          env:
          - name: SECRET_KEY
            value: "my-secret-key"
```

This should work, but we will still see errors in logs because we Django will attempt to establish a connection with the Postgres database which we will be setting up next.

We can hit our public facing `hello-world` endpoint which should serve as a nice health check for the Django container.

Let's test this endpoint with `curl`. We haven't set up a Kubernetes `Service` yet, so we will have to curl the Django application from within the cluster. We can do this with:

```
k exec django-backend-757b5944d8-htssm -- curl -s http://172.17.0.5/api/hello-world/
```

This gives us:

```
command terminated with exit code 7
```

Our container has started, but the database connection has prevented the Django process from starting. In our Pod logs, we can see that no request have been received and the Django application is not listening on `0.0.0.0:8000`.

Let's come back to this once we have set up our Postgres database.

## Postgres

First, we create a `PersistentVolume` resource:

**`kubernetes/postgres/volume.yml`**

```yml
kind: PersistentVolume
apiVersion: v1
metadata:
  name: postgres-pv
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/postgres-pv
```

::: warning storageClassName
Clicking on the `storageClassName` gave a 404 error
:::

::: warning Authentication failure
Message with postgres authentication failure
:::

After changing the `postgres` user password, the migrations are able to run successfully:

```bash
k exec django-784d668c8b-9gbf7 -it -- ./manage.py migrat
e
loading minikube settings...
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, sessions, social_django
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying accounts.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying sessions.0001_initial... OK
  Applying social_django.0001_initial... OK
  Applying social_django.0002_add_related_name... OK
  Applying social_django.0003_alter_email_max_length... OK
  Applying social_django.0004_auto_20160423_0400... OK
  Applying social_django.0005_auto_20160727_2333... OK
  Applying social_django.0006_partial... OK
  Applying social_django.0007_code_timestamp... OK
  Applying social_django.0008_partial_timestamp... OK
```

::: warning Try this again
Try this again with a clean version of minikube and using the Secrets resource.
:::

I initially started the postgres container with a password set by environment variable. This may have set data in the

::: tip kubectl cheatsheet from kubernetes documentation
[https://kubernetes.io/docs/reference/kubectl/cheatsheet/#viewing-finding-resources](https://kubernetes.io/docs/reference/kubectl/cheatsheet/#viewing-finding-resources)
:::


Show the service in kubernetes:

```
minikube service kubernetes-django-service
```

We have two options for how to run the frontend application in Kubernetes.

1) Servce the static content from Django
2) Serve the static content from nginx and use another service.

Serving the static content from Django was not working, so I'm building another deployment/service for frontend. For this to work, we need to tell Quasar about the address for the Django service. There are two ways to do this:

1) DNS
2) Environment variables


## Use environment variables to get service IP/Host

This won't be possible with out static front end site.

## Use DNS for services

DNS will be easier since we are building static assets outside of the context of Kubernetes and the environment variables that it injects at runtime.

```
/ # curl http://kubernetes-django-service:8000/api/
{"message": "Root"}
```

We need to set the `DOMAIN_NAME` environment variable to `kubernetes-django-service`, and also set the port, and we should be able to access the backend from frontend AJAX calls.