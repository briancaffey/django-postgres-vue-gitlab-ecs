# Helm

This section will build on the previous section that built the application in minikube.

> Helm helps you manage Kubernetes applications — Helm Charts help you define, install, and upgrade even the most complex Kubernetes application.

After reading this section, you will be able to run one command to install the application on minikube using Helm.

I'll be using the Helm documentation, starting with the [Quickstart Guide](https://helm.sh/docs/using_helm/#quickstart)

First, make sure we are using minikube:

```
k config current-context
minikube
```

Next, initialize helm in minikube:

```
helm init --history-max 200
Creating /home/brian/.helm
Creating /home/brian/.helm/repository
Creating /home/brian/.helm/repository/cache
Creating /home/brian/.helm/repository/local
Creating /home/brian/.helm/plugins
Creating /home/brian/.helm/starters
Creating /home/brian/.helm/cache/archive
Creating /home/brian/.helm/repository/repositories.yaml
Adding stable repo with URL: https://kubernetes-charts.storage.googleapis.com
Adding local repo with URL: http://127.0.0.1:8879/charts
$HELM_HOME has been configured at /home/brian/.helm.

Tiller (the Helm server-side component) has been installed into your Kubernetes Cluster.

Please note: by default, Tiller is deployed with an insecure 'allow unauthenticated users' policy.
To prevent this, run `helm init` with the --tiller-tls-verify flag.
For more information on securing your installation see: https://docs.helm.sh/using_helm/#securing-your-helm-install
ation
```

I'm also going to be using this guide: [https://docs.bitnami.com/kubernetes/how-to/create-your-first-helm-chart/](https://docs.bitnami.com/kubernetes/how-to/create-your-first-helm-chart/)

Let's use the `helm create` command:

```
helm create myhelm
Creating myhelm
```

Let's look at the files this generates:

```
tree myhelm
myhelm
├── charts
├── Chart.yaml
├── templates
│   ├── deployment.yaml
│   ├── _helpers.tpl
│   ├── ingress.yaml
│   ├── NOTES.txt
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml

3 directories, 8 files
```

`templates` is the directory where Kubernetes resource files are stored. We can see a deployment, a service and an ingress resource are pre-populated as an example.

Let's take a look at what the Helm release would look like with a dry-run:

```
helm install ./mychart --debug --dry-run
[debug] Created tunnel using local port: '45219'

[debug] SERVER: "127.0.0.1:45219"

[debug] Original chart version: ""
[debug] CHART PATH: /home/brian/gitlab/django-postgres-vue-gitlab-ecs/mychart

NAME:   idolized-grizzly
REVISION: 1
RELEASED: Mon Sep 30 21:05:02 2019
CHART: mychart-0.1.0
USER-SUPPLIED VALUES:
{}

COMPUTED VALUES:
affinity: {}
fullnameOverride: ""
image:
  pullPolicy: IfNotPresent
  repository: nginx
  tag: stable
imagePullSecrets: []
ingress:
  annotations: {}
  enabled: false
  hosts:
  - host: chart-example.local
    paths: []
  tls: []
nameOverride: ""
nodeSelector: {}
replicaCount: 1
resources: {}
service:
  port: 80
  type: ClusterIP
tolerations: []

HOOKS:
---
# idolized-grizzly-mychart-test-connection
apiVersion: v1
kind: Pod
metadata:
  name: "idolized-grizzly-mychart-test-connection"
  labels:
    app.kubernetes.io/name: mychart
    helm.sh/chart: mychart-0.1.0
    app.kubernetes.io/instance: idolized-grizzly
    app.kubernetes.io/version: "1.0"
    app.kubernetes.io/managed-by: Tiller
  annotations:
    "helm.sh/hook": test-success
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args:  ['idolized-grizzly-mychart:80']
  restartPolicy: Never
MANIFEST:

---
# Source: mychart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: idolized-grizzly-mychart
  labels:
    app.kubernetes.io/name: mychart
    helm.sh/chart: mychart-0.1.0
    app.kubernetes.io/instance: idolized-grizzly
    app.kubernetes.io/version: "1.0"
    app.kubernetes.io/managed-by: Tiller
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: mychart
    app.kubernetes.io/instance: idolized-grizzly
---
# Source: mychart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: idolized-grizzly-mychart
  labels:
    app.kubernetes.io/name: mychart
    helm.sh/chart: mychart-0.1.0
    app.kubernetes.io/instance: idolized-grizzly
    app.kubernetes.io/version: "1.0"
    app.kubernetes.io/managed-by: Tiller
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: mychart
      app.kubernetes.io/instance: idolized-grizzly
  template:
    metadata:
      labels:
        app.kubernetes.io/name: mychart
        app.kubernetes.io/instance: idolized-grizzly
    spec:
      containers:
        - name: mychart
          image: "nginx:stable"
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {}
```

This created a dry-run that shows use the resource yaml files that would have been generated. Notice that the name of the release is `idolized-grizzly`, and we can see that this name has been injected into the yaml templates. `dry-run` does not guarantee that these resources will be accepted by the Kubernetes API, however.

Let's look at the Service:

```
# Source: mychart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: idolized-grizzly-mychart
...
```

Now let's compare this to the corresponding part of `helm/templates/service.yml`:

```
apiVersion: v1
kind: Service
metadata:
  name: {{ include "mychart.fullname" . }}
```

`mychart.fullname` is a function that is defined in `_helpers.tpl`:

```yml
{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}
```

Let's talk about the template language


```html
<div>
  {{ .Title }}
</div>
```

Results in

```html
<div>
  Hello, World!
</div>
```

```html
<div>
  {{- .Title -}}
</div>

```

```html
<div>Hello, World!</div>
```

Let's start by adding the following files to the `templates` directory:

- `gunicorn.deployment.yaml`
- `gunicorn.service.yaml`

Change the template values in these two files and add the necessary values to `values.yaml`.

Next, let's build the `backend` image:

```
eval $(minikube docker-env)
docker-compose -f compose/minikube.yml build backend
```

Now let's install the this simple chart to see if things are working correctly:

```
helm install ./mychart
NAME:   whopping-dragon
LAST DEPLOYED: Tue Oct  1 00:20:46 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Deployment
NAME                     READY  UP-TO-DATE  AVAILABLE  AGE
whopping-dragon-mychart  0/1    1           0          0s

==> v1/Pod(related)
NAME                                      READY  STATUS             RESTARTS  AGE
whopping-dragon-mychart-78884d684f-5vxjb  0/1    ContainerCreating  0         0s

==> v1/Service
NAME                     TYPE      CLUSTER-IP     EXTERNAL-IP  PORT(S)         AGE
whopping-dragon-mychart  NodePort  10.98.181.234  <none>       8000:30399/TCP  0s


NOTES:
1. Get the application URL by running these commands:
```

We can inspect the release with the following command:

```
helm list
NAME            REVISION        UPDATED                         STATUS          CHART           APP VERSION     NAMESPACE
foppish-badger  1               Tue Oct  1 00:14:58 2019        DEPLOYED        mychart-0.1.0   1.0             default
```

Then we can delete the release with the following command:

```
helm delete foppish-badger
release "foppish-badger" deleted
```

