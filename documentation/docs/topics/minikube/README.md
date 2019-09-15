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
          command: ["./manage.py", "runserver", "0.0.0.0:8000"]
          ports:
          - containerPort: 8000
```

::: warning No environment variables
**Note**: the pod template in this deployment definition does not have any environment variables. We will need to add environment variables for sensitive information such as the Postgres username and password. We will add these shortly.
:::

There is one line in the above resource definition that makes everything work with minikube and the docker images we have just built: `imagePullPolicy: IfNotPresent`. This line tells Kubernetes to pull the image (from Docker Hub, or another registry if specified) **only** if the image is not present locally. If we didn't set the `imagePullPolicy` to `IfNotPresent`, Kubernetes would try to pull the image from docker hub, which would probably fail, resulting in an `ErrImagePull`.

::: warning Don't configure the deployment yet!

We would run the following command to configure this deployment.
```
kubectl apply -f kubernetes/django/deployment.yml
```

We haven't created the secrets that Django needs yet for access to the Postgres database, save this file and we will come back to it after we configure Postgres in our minikube Kubernetes cluster.
:::

## Postgres

Using Postgres in our minikube cluster will involve the following resources:

- secrets
- persistent volume
- persistent volume claim
- deployment
- service

### Secrets

Secrets should be base64 encoded because they can contain either strings or raw bytes. Here's an example of how we can encode `my-secret-string` with base64 encdoding:

```
echo -n "my-secret-string" | base64
bXktc2VjcmV0LXN0cmluZw==
```

We will use `bXktc2VjcmV0LXN0cmluZw==` in our `secrets.yml` file. We shouldn't commit any sensitive information in secrets files. base64 encdoing is not encrypted, the value can be decoded read as `my-secret-string`:

```
echo -n "bXktc2VjcmV0LXN0cmluZw==" | base64 -d
my-secret-string
```

Choose a username and password for your Postgres database and enter both of them as base64-encoded values:

**`kubernetes/postgres/secrets.yml`**

```
apiVersion: v1
kind: Secret
metadata:
  name: postgres-credentials
type: Opaque
data:
  user: YnJpYW4=
  password: cGFzc3dvcmQx
```

You can open the minikube dashboard with `minikube dashboard` and view the secret values after you send this file to the kubernetes API with:

```
k apply -f kubernetes/postgres/secrets.yml
```

### Persistent Volume

Next, we need to configure a volume to persist data that will be stored in the postgres database.

In minikube, since we are only using a single-node cluster, it is OK to use a `hostPath` volume:

**`kubernetes/postgres/volume.yml`**

```
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

::: tip Remember
Persistent Volumes are not namespaced in Kubernetes
:::

### Persistent Volume Claim

Next we will make a persistent volume claim that we can reference in the postgres deployment:

**`kubernetes/postgres/volume_claim.yml`**

```
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: postgres-pvc
  labels:
    type: local
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
  volumeName: postgres-pv
```

The `storageClassName` is arbitrary; it only needs to be the *same* value in order for the PVC to get access to the storage it needs.

### Deployment

Now we can create the Postgres deployment. This will use our secrets and persistent volumes:

**`kubernetes/postgres/deployment.yml`**

```
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: postgres-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres-container
  template:
    metadata:
      labels:
        app: postgres-container
        tier: backend
    spec:
      containers:
        - name: postgres-container
          image: postgres:9.6.6
          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: user

            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password

          ports:
            - containerPort: 5432
          volumeMounts:
            - name: postgres-volume-mount
              mountPath: /var/lib/postgresql/data

      volumes:
        - name: postgres-volume-mount
          persistentVolumeClaim:
            claimName: postgres-pvc
```

Finally, we can create a service that will allow us to access the Postgres database from pods in our Django deployment (which we will come back to next):

**`kubernetes/postgres/service.yml`**

```
kind: Service
apiVersion: v1
metadata:
  name: postgres
spec:
  selector:
    app: postgres-container
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
```

## Django Webserver

### Deployment

Next let's come back to the deployment that will serve requests for our Django API. As mentioned earlier, this needs to be configured with some additional environment variables. Some of these environment variables will be added explicitly, and some will be added automatically by Kubernetes for simple and easy service discovery.

Here's the full deployment definition for our Django deployment:

**`kubernetes/django/deployment.yml`**

```
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: django
spec:
  replicas: 1
  selector:
    matchLabels:
      app: django-container
  template:
    metadata:
      labels:
        app: django-container
    spec:
      containers:
        - name: backend
          imagePullPolicy: IfNotPresent
          image: backend:11
          command: ["./manage.py", "runserver", "0.0.0.0:8000"]
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8000
          readinessProbe:
            # an http probe
            httpGet:
              path: /readiness
              port: 8000
            initialDelaySeconds: 10
            timeoutSeconds: 5
          ports:
          - containerPort: 8000
          env:
            - name: DJANGO_SETTINGS_MODULE
              value: 'backend.settings.minikube'

            - name: SECRET_KEY
              value: "my-secret-key"

            - name: POSTGRES_NAME
              value: postgres

            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: user

            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password

    # I'm not sure that we need these volumes, but they were included in the tutorial referenced at the beginning of this guide.

          volumeMounts:
            - name: postgres-volume-mount
              mountPath: /var/lib/busybox

      volumes:
        - name: postgres-volume-mount
          persistentVolumeClaim:
            claimName: postgres-pvc
```

Let's notice the additions to our Django deployment. First, we see an array of environment variables:

- `DJANGO_SETTINGS_MODULE`: this tells Django which settings module to use. It is set to `backend.settings.minikube`, which means that we are using the settings file `backend/settings/minikube.py`
- `SECRET_KEY`: Django needs a secret key to start (this should also be configured as a secret...)
- `POSTGRES_NAME`: we are using the default `postgres` database
- `POSTGRES_USER` and `POSTGRES_PASSWORD`: these environment variables that we are

Let's look at the `minikube.py` settings file:

**`backend/settings/minikube.py`**

```python
from .development import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME', 'kubernetes_django'), # noqa
        'USER': os.environ.get('POSTGRES_USER', 'postgres'), # noqa
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'), # noqa
        'HOST': os.environ.get('POSTGRES_SERVICE_HOST', 'postgres'), # noqa
        'PORT': os.environ.get('POSTGRES_SERVICE_PORT', 5432), # noqa
    }
}
```

Notice that in the `DATABASES` section we see the Postgres name, user and password environment variables that we added to the deployment's pod template.

`POSTGRES_SERVICE_HOST` and `POSTGRES_SERVICE_PORT` are added automatically. Kubernetes adds a set of environment variables for all services in the namespace that include the service IP and the service port of the service. Environment variables are one of two ways to do this type of simple service discovery.

Also, take note of the addition of the `livenessProbe` and `readinessProbe` keys in the container definition of the pod template. These tell kubelet to send HTTP requests to `/healthz` and `/readiness` which are used to evaluate the health and readiness of the Django deployment, respectively. We will come back to these to see exactly how they work by sabotaging our Django deployment in different ways.

See [this article](https://www.ianlewis.org/en/kubernetes-health-checks-django) as a reference for how health checks have been implemented using Django middleware.

### Service

Now that we have a deployment for our Django webserver, let's create a service that will allow us to reach it:

**`kubernetes/django/service.yml`**

```
kind: Service
apiVersion: v1
metadata:
  name: kubernetes-django-service
spec:
  selector:
    app: django-container
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: NodePort
```

This needs to do two things: match the `django-container` label that is present in the Django deployment pod template, and specify port `8000` that our Django webserver is listening on, and that the pod has configured with `containerPort: 8000`.

We are almost ready to apply our Django deployment and service, but before we do that we need migrate our database by running `./manage.py migrate`. The migration should be ran once, and it must run successfully. This type of task can be handled by a Kubernetes Job.

**`kubernetes/django/migration.yml`**

```
apiVersion: batch/v1
kind: Job
metadata:
  name: django-migrations
spec:
  template:
    spec:
      containers:
        - name: django
          image: backend:2
          command: ['python', 'manage.py', 'migrate']
          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: user

            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password

            - name: POSTGRES_NAME
              value: postgres

            - name: DJANGO_SETTINGS_MODULE
              value: 'backend.settings.minikube'

      restartPolicy: Never
  backoffLimit: 5
```

Configure the job by running the following command:

```
k apply -f kubernetes/django/migration.yml
```

Now let's inspect our pods

TODO: show pods

```
k get pods

```

TODO: show pod logs

Now let's look at the Job's pod logs:

```
k logs ....

```

We can see that our database migrations did indeed run successfully. Now we can configure the Django service and deployment with the following command:

```
k apply -f kubernetes/django/
```

Visit the Django admin panel by running the following command:

```
minikube service kubernetes-django-service
```

and then navigate to `/admin`, and you should see the Django admin login page. Let's create a default user. I have a management command which we can run:

TODO: show k exec

```
k exec ... -it -- ./manage.py create_default_user

```

You could also replace my `create_default_user` command with `createsuperuser` and create a user that way.

Login with your user to verify that everything is working properly.

## Frontend

Now that the Django backend is working, let's take a look at the front end client that is built with Vue and Quasar Framework. As we did with the backend, we will build the frontend container with the `compose/minikube.py` file. Let's look at the frontend service definition in that file:

**`compose/minikube.yml`**

```
version: '3.7'

services:

  frontend:
    image: frontend:1
    build:
      context: ../
      dockerfile: nginx/minikube/Dockerfile
      args:
        - DOMAIN_NAME=minikube.local
        - GOOGLE_OAUTH2_KEY=google123
        - GITHUB_KEY=github123
        - WS_PROTOCOL=ws
        - HTTP_PROTOCOL=http
```

Make sure that your current shell has the correct environment variables set for the `DOCKER_HOST` by running:

```
eval $(minikube docker-env)
```

Build the image with the following command:

```
docker-compose -f compose/minikube.yml build frontend
```

Notice that we set `DOMAIN_NAME` to be `minikube.local`. We will use this address to access both the frontend and backend service once we configure an Ingress for our minikube Kubernetes cluster.

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
