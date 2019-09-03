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
docker-compose build backend
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