# Minikube

Minikube is a tool for running a single-node Kubernetes cluster inside of a virtual machine. It is a popular tool for developing Kubernetes applications locally.

This topic will cover using `minikube` to set up the project Kubernetes locally.

::: tip Goal
By the end of this guide, you will be able to:

1. Navigate to `http://minikube.local` in your browser and interact with the application running in **minikube** in the same way that you would with the application running using **docker-compose** for local development.

1. Run **Cypress** tests against the application running in **minikube** to verify that everything is working correctly.
:::

I'll be following [this great guide](https://medium.com/@markgituma/kubernetes-local-to-production-with-django-1-introduction-d73adc9ce4b4) to get started, making changes and additions where necessary.

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

## Building Images

We will need to build two images from our code:

1. The `backend` image that will run the Django server, Django Channels, Celery and Beat
1. The `frontend` image that will contains nginx for serving our Quasar frontend application.

Both of these images will need environment variables. We will use `docker-compose` to easily manage the building and environment variable management. Read [this article](https://vsupalov.com/docker-arg-env-variable-guide/) for more information. You don't absolutely have to user docker-compose to build the images, but it should keep things straightforward and easy to understand.

Remember that that the docker CLI, like `kubectl`, send requests to a REST API. When we run `minikube start`, this configures `kubectl` to send commands to the Kubernetes API server that is running inside of the minikube virtual machine. Similarly, we need to tell our docker CLI that we want to send API calls that the docker CLI command makes to the docker daemon running in the minikube VM, **not** the docker daemon on our local machine (even though the files from which we build our images are on our local machine and not on the minikube VM's file system). We can configure our docker CLI to point to the minikube VM with the following command:

```
eval $(minikube docker-env)
```

Now run `docker ps` and you will see many different containers that Kubernetes uses internally.

To point the docker CLI back at your local docker daemon, run:

```
eval $(minikube docker-env -u)
```

Let's look at what the command is doing:

`$(minikube docker-env)` results in the following output:

```bash
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="/home/brian/.minikube/certs"
# Run this command to configure your shell:
# eval $(minikube docker-env)
```

Notice that the `DOCKER_HOST` is pointing to the minikube VM on docker's default port `2376`. `eval` executes these commands, setting the environment variables in the *current shell* by using `export`. If you switch to another shell, you will need to rerun this command if you want to run docker commands against minikube's docker daemon.

With these environment variables set, let's build the Django container image with the following command:

```sh
docker-compose -f compose/minikube.yml build backend
```

Here's the `backend` service defined in `compose/minikube.yml`:

```yml
  backend:
    image: backend:1
    build:
      context: ../backend/
      dockerfile: scripts/dev/Dockerfile
```

**`kubernetes/django/deployment.yml`**

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
          imagePullPolicy: IfNotPresent
          image: backend:1
          command: ["./manage.py", "runserver"]
          ports:
          - containerPort: 8000
```

::: warning No environment variables
**Note***: the pod template in this deployment definition does not have any environment variables. We will need to add environment variables for sensitive information such as the Postgres username and password. We will add these shortly
:::

There is one line in the above resource definition that makes everything work with minikube and the docker images we have just built: `imagePullPolicy: IfNotPresent`. This line tells Kubernetes to pull the image (from Docker Hub, or another registry if specified) **only** if the image is not present locally. If we didn't set the `imagePullPolicy` to `IfNotPresent`, Kubernetes would try to pull the image from docker hub, which would probably fail, resulting in an `ErrImagePull`.

Let's send this file to the minikube Kubernete API server with the following command:

```
kubectl apply -f kubernetes/django/deployment.yml
```

Your pod for the deployment should be starting. Inspect the pods with `k get pods`.

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

## Secrets

Let's use base64 encoding to define a username and password for our Postgres username and password:

```
echo -n "my-string" | base64
```



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

This works from inside of a pod, but we can't use this for our static site since `localhost` won't know how to resolve `kubernetes-django-service`. One solution for this is to get the `port:ip` of the backend service from minikube, and then use this value for the `baseUrl` in our frontend application:

**minikube/Dockerfile**

Use the following command to build the frontend resources in minikube:

```
docker-compose -f compose/minikube.yml build frontend
```

Make sure that your current shell has the correct environment variables set for the `DOCKER_HOST` by running:

```
eval $(minikube docker-env)
```

We can pass the environment variables needed during the build process with `ARG` and `ENV`.

For `DOMAIN_NAME`, want to use an address that will point to the minikube Kubernetes cluster. Since the IP might change, we can set this to a named domain such as `test.dev`, and add a line to `/etc/hosts` that will point `test.dev` to the minikube IP. Then, we will need to setup a ingress to point `test.dev` to our `kubernetes-django-service` service.

## Troubleshooting and Misc

https://stackoverflow.com/questions/55573426/virtualbox-is-configured-with-multiple-host-only-adapters-with-the-same-ip-whe

## Enable Ingress Addon in Minikibe

```sh
minikube addons enable ingress
```

With the Ingress enabled, we can add an `Ingress` resource:

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-test
spec:
  rules:
  - host: minikube.local
    http:
      paths:
      - path: /api/
        backend:
          serviceName: kubernetes-django-service
          servicePort: 8000
      - path: /admin/
        backend:
          serviceName: kubernetes-django-service
          servicePort: 8000
      - path: /static/
        backend:
          serviceName: kubernetes-django-service
          servicePort: 8000
      - path: /
        backend:
          serviceName: kubernetes-frontend-service
          servicePort: 80
```

Also, we need to add an entry to `/etc/hosts` so that requests to `minikube.local` will be forwarded to the `minikube ip`:

```sh
192.168.99.106  minikube.local
```

## Health Checks

We can add readiness and liveness checks for Django backend container. Liveness will check that the container has not crashed. Readiness will check that the container is ready to accept traffic by checking that postgres and redis are ready to accept connections.

Here are the checks in the `container` spec:

```yml
    livenessProbe:
    httpGet:
        path: /healthz
        port: 8000
    readinessProbe:

    httpGet:
        path: /readiness
        port: 8000
    initialDelaySeconds: 20
    timeoutSeconds: 5
```

See [this article](https://www.ianlewis.org/en/kubernetes-health-checks-django) as a reference for how health checks have been implemented.

## Celery

Next, let's add a deployment for Celery.

::: warning TODO
Not finished
:::

## Websockets

Next, let's add a deployment for Django Channels.

::: warning TODO
Not finished
:::

## Cypress tests against the minikube cluster

Now that we have implemented all parts of our application in minikube, let's run our tests against the cluster. Run the following command to open Cypress:

```
$(npm bin)/cypress open --config baseUrl=http://minikube.local
```

Click `Run all specs` and make sure there are no errors in the test results.
