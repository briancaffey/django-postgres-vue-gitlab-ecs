# Deploying on GCP with Terraform and GitLab

This guide provides an overview of how to deploy the project on GCP using Terraform and GitLab.

## Research

Here are some recent guides that come up when you search for "gke and terraform".

- [https://elastisys.com/2019/04/12/kubernetes-on-gke-from-scratch-using-terraform/](https://elastisys.com/2019/04/12/kubernetes-on-gke-from-scratch-using-terraform/)

- [https://www.padok.fr/en/blog/kubernetes-google-cloud-terraform-cluster](https://www.padok.fr/en/blog/kubernetes-google-cloud-terraform-cluster)

- [https://github.com/jetstack/terraform-google-gke-cluster](https://github.com/jetstack/terraform-google-gke-cluster)

This guide will compare and contrast different ways of deploying a GKE cluster with Terraform as described in these resources.

## Elastisys

### Overview

1. Install Terraform
1. Install `kubectl`
1. Install the Google Cloud SDK
1. Clone the [repo](https://github.com/llarsson/gke-cluster-terraform)

#### Install Terraform

```
sudo snap install terraform
terraform v0.11.11 from Nathan Handler (nhandler) installed
terraform --version
Terraform v0.11.11
```

### Create a Service Account for Terraform

In the Google Cloud Console go to `IAM` > `Service Accounts`, and then add a service account with the name `terraform`.

Next, give it the following Roles:

- Kubernetes Engine Admin (Full management of Kubernetes Clusters and their Kubernetes API objects.)
- Storage Admin (Full control of GCS resources.)

Next, download a JSON key for this service account and save it somewhere secure such as Google Drive.

Take the file and rename it to `account.json` and put it in the `terraform` directory (it will not be tracked in git)

### Create a Google Storage bucket and enable storage

I have created one called `verbose-equals-true-tf`.

Update the value of `terraform` > `backend` > `bucket` in `terraform/google.tf` with the name of the bucket you have chosen.

Next, enable **versioning** on the bucket:

```bash
export BUCKET_ID=verbose-equals-true-tf
gsutil versioning set on gs://${BUCKET_ID}
# verify that versioning has been enabled for the bucket
gsutil versioning get gs://${BUCKET_ID}
```

### Configuring Google Cloud Storage as Terraform remote state

Run these commands in the `terraform` directory

```
export ENVIRONMENT=production
terraform workspace new ${ENVIRONMENT}
terraform init -var-file=${ENVIRONMENT}.tfvars

Initializing the backend...

Successfully configured the backend "gcs"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Checking for available provider plugins on https://releases.hashicorp.com...
- Downloading plugin for provider "google" (2.17.0)...

The following providers do not have any version constraints in configuration,
so the latest version was installed.

To prevent automatic upgrades to new major versions that may contain breaking
changes, it is recommended to add version = "..." constraints to the
corresponding provider blocks in configuration, with the constraint strings
suggested below.

* provider.google: version = "~> 2.17"

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

### Giving our Service Account required permissions

We need to give our service account the required permissions, specifically, the `roles/editor` role. To do this, run the following commands:

```
export PROJECT=verbose-equals-true
export SERVICE_ACCOUNT=terraform
gcloud projects add-iam-policy-binding ${PROJECT} --member serviceAccount:${SERVICE_ACCOUNT}@${PROJECT}.iam.gserviceaccount.com --role roles/editor

Updated IAM policy for project [verbose-equals-true].
bindings:
- members:
  - serviceAccount:service-1000150547972@compute-system.iam.gserviceaccount.com
  role: roles/compute.serviceAgent
- members:
  - serviceAccount:terraform@verbose-equals-true.iam.gserviceaccount.com
  role: roles/container.admin
- members:
  - serviceAccount:service-1000150547972@container-engine-robot.iam.gserviceaccount.com
  role: roles/container.serviceAgent
- members:
  - serviceAccount:1000150547972-compute@developer.gserviceaccount.com
  - serviceAccount:1000150547972@cloudservices.gserviceaccount.com
  - serviceAccount:service-1000150547972@containerregistry.iam.gserviceaccount.com
  - serviceAccount:terraform@verbose-equals-true.iam.gserviceaccount.com
  role: roles/editor
- members:
  - user:briancaffey2010@gmail.com
  role: roles/owner
- members:
  - serviceAccount:terraform@verbose-equals-true.iam.gserviceaccount.com
  role: roles/storage.admin
etag: BwWUz3Od8KY=
version: 1
```

### Deploying the GKE cluster

Now that everything is configured properly, deploying the Kubernetes cluster can be done with the following command:

```
terraform apply -var-file=${ENVIRONMENT}.tfvars
```

Type `yes` to confirm.

The cluster will take some time to come up. It will also restart itself with the custom node pool that is defined in Terraform.

### Using Helm in GKE

Let's install Helm in our cluster. This guide shows how to setup Tiller with a service account so that it will be authorized to create resources in our cluster.

#### Create service account for helm

Create the following service account:



```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: helm
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: helm
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: helm
    namespace: kube-system
```

```
k apply -f k8s/service-account.yaml
serviceaccount/helm created
clusterrolebinding.rbac.authorization.k8s.io/helm created
```

If this is successful, initialize Helm with the following command:

```
helm init --service-account helm
```


https://medium.com/google-cloud/helm-on-gke-cluster-quick-hands-on-guide-ecffad94b0

Let's list the pods in the `kube-system` namespace to see if Tiller is running:

```
k get pods -n kube-system
NAME                                                             READY   STATUS    RESTARTS   AGE
calico-node-gn4ks                                                2/2     Running   0          35m
calico-node-jvvwz                                                2/2     Running   0          35m
calico-node-stljj                                                2/2     Running   0          35m
calico-node-vertical-autoscaler-579467d76c-d77g8                 1/1     Running   2          43m
calico-typha-65bfd5544b-vhq2v                                    1/1     Running   0          35m
calico-typha-horizontal-autoscaler-847fc7bc8d-kznjt              1/1     Running   0          43m
calico-typha-vertical-autoscaler-dc95cc498-wxssj                 1/1     Running   3          43m
event-exporter-v0.2.4-5f88c66fb7-kwn27                           2/2     Running   0          43m
fluentd-gcp-scaler-59b7b75cd7-ssvtc                              1/1     Running   0          38m
fluentd-gcp-v3.2.0-2zxbs                                         2/2     Running   0          37m
fluentd-gcp-v3.2.0-cvdzj                                         2/2     Running   0          37m
fluentd-gcp-v3.2.0-pc4gz                                         2/2     Running   0          36m
heapster-v1.6.1-5b4cb58d8f-bbkm4                                 3/3     Running   0          35m
ip-masq-agent-j8l4c                                              1/1     Running   0          37m
ip-masq-agent-s4p8s                                              1/1     Running   0          37m
ip-masq-agent-tqbmb                                              1/1     Running   0          36m
kube-dns-79868f54c5-f2ldj                                        4/4     Running   0          43m
kube-dns-79868f54c5-slzbp                                        4/4     Running   0          43m
kube-dns-autoscaler-bb58c6784-tt446                              1/1     Running   0          43m
kube-proxy-gke-verbose-equals-t-verbose-equals-t-a5fdda87-btk8   1/1     Running   0          37m
kube-proxy-gke-verbose-equals-t-verbose-equals-t-cc7974e9-h64g   1/1     Running   0          37m
kube-proxy-gke-verbose-equals-t-verbose-equals-t-faeb6a69-tcnz   1/1     Running   0          36m
l7-default-backend-fd59995cd-wzqsr                               1/1     Running   0          43m
metrics-server-v0.3.1-57c75779f-pqr7c                            2/2     Running   0          43m
prometheus-to-sd-4945c                                           1/1     Running   0          36m
prometheus-to-sd-qqdv4                                           1/1     Running   0          36m
prometheus-to-sd-zvzdg                                           1/1     Running   0          36m
tiller-deploy-57f498469-9ck5t                                    1/1     Running   0          6m58s
```

Install Postgres with the Bitnami Helm Chart


### Deploying to Terraform from GitLab CI

Now that we can deploy Terraform resources from the command line, let's automate this in our GitLab CI pipeline.

First, we need to save our `account.json` file in our GitLab CI variables. This can be done with the following commands:

```
cat terraform/account.json | base64 -w0
```

Here are some resources showing how to use Terraform and in GitLab CI


::: warning In progress
This section is not complete. Updates coming soon.
:::

