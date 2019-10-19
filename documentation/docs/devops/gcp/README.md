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

Install a specific version of Terraform:

```
wget https://releases.hashicorp.com/terraform/0.12.10/terraform_0.12.10_linux_amd64.zip
unzip terraform_0.12.10_linux_amd64.zip
chmod +x terraform
sudo mv terraform /usr/local/bin/
terraform --version
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

### Install Postgres with the Bitnami Helm Chart


Here is a slightly outdated guide from Bitnami that shows how to install postgres with Helm:

[https://engineering.bitnami.com/articles/create-a-production-ready-postgresql-cluster-bitnami-kubernetes-and-helm.html](https://engineering.bitnami.com/articles/create-a-production-ready-postgresql-cluster-bitnami-kubernetes-and-helm.html)


First, download the `values-production.yaml` file using the following command:

```
curl -O https://raw.githubusercontent.com/helm/charts/master/stable/wordpress/values-production.yaml
```

I had to change one value to disable monitoring:

```
metrics:
  enabled: false
```

See the command below that sets this value in a CLI parameter.

To deploy the `stable/postgres` chart, run the following command.

```
helm install --name my-postgres stable/postgresql \
    -f values-production.yaml \
    --set postgresqlPassword=ROOT_PASSWORD \
    --set replication.password=REPLICATION_PASSWORD
    --set metrics.enabled=false
```
### How to delete all resources


The `stable/helm` release creates several resources:

- services
- statefulsets
- persistentvolumes
- pvc

Also, GCP will dynamically provision disks that are used by the PVs. We can list these with

```
gcloud compute disks list
NAME                                                             LOCATION       LOCATION_SCOPE  SIZE_GB  TYPE         STATUS
gke-verbose-equals-t-verbose-equals-t-379740c0-0c5j              us-central1-c  zone            100      pd-standard  READY
gke-verbose-equals-tru-pvc-2b60b760-ee20-11e9-afd8-42010a800fe4  us-central1-c  zone            8        pd-standard  READY
gke-verbose-equals-t-verbose-equals-t-dee69f6e-9w5h              us-central1-b  zone            100      pd-standard  READY
gke-verbose-equals-tru-pvc-0b603b57-ee20-11e9-afd8-42010a800fe4  us-central1-b  zone            8        pd-standard  READY
gke-verbose-equals-t-verbose-equals-t-0604b9f8-n9xc              us-central1-f  zone            100      pd-standard  READY
gke-verbose-equals-tru-pvc-0b6f922a-ee20-11e9-afd8-42010a800fe4  us-central1-f  zone            8        pd-standard  READY
```

The 100GB disks are provisioned for the nodes in our cluster, and the 8GB nodes are provisioned for the PVs.

When we delete the helm release with the following command:

```
helm delete my-release
```

The PVs and PVCs are not deleted. They *persist*. Let's show this:

```
k get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                          STORAGECLASS   REASON   AGE
pvc-0b603b57-ee20-11e9-afd8-42010a800fe4   8Gi        RWO            Delete           Bound    default/data-my-postgres-postgresql-slave-0    standard                25h
pvc-0b6f922a-ee20-11e9-afd8-42010a800fe4   8Gi        RWO            Delete           Bound    default/data-my-postgres-postgresql-master-0   standard                25h
pvc-2b60b760-ee20-11e9-afd8-42010a800fe4   8Gi        RWO            Delete           Bound    default/data-my-postgres-postgresql-slave-1    standard                25h
```

```
k describe pv pvc-0b603b57-ee20-11e9-afd8-42010a800fe4
Name:              pvc-0b603b57-ee20-11e9-afd8-42010a800fe4
Labels:            failure-domain.beta.kubernetes.io/region=us-central1
                   failure-domain.beta.kubernetes.io/zone=us-central1-b
Annotations:       kubernetes.io/createdby: gce-pd-dynamic-provisioner
                   pv.kubernetes.io/bound-by-controller: yes
                   pv.kubernetes.io/provisioned-by: kubernetes.io/gce-pd
Finalizers:        [kubernetes.io/pv-protection]
StorageClass:      standard
Status:            Bound
Claim:             default/data-my-postgres-postgresql-slave-0
Reclaim Policy:    Delete
Access Modes:      RWO
VolumeMode:        Filesystem
Capacity:          8Gi
Node Affinity:
  Required Terms:
    Term 0:        failure-domain.beta.kubernetes.io/zone in [us-central1-b]
                   failure-domain.beta.kubernetes.io/region in [us-central1]
Message:
Source:
    Type:       GCEPersistentDisk (a Persistent Disk resource in Google Compute Engine)
    PDName:     gke-verbose-equals-tru-pvc-0b603b57-ee20-11e9-afd8-42010a800fe4
    FSType:     ext4
    Partition:  0
    ReadOnly:   false
Events:         <none>
```

Note that the `PDName` for the PV we described is one of the 8GB disks that was automatically provisioned.

Let's delete the Kubernetes cluster and see what happens to the PDs.

Run

```
terraform destroy -var-file=production.tfvars
Acquiring state lock. This may take a few moments...
google_container_cluster.cluster: Refreshing state... [id=verbose-equals-true-cluster]
google_container_node_pool.general_purpose: Refreshing state... [id=us-central1/verbose-equals-true-cluster/verbose-equals-true-general]

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # google_container_cluster.cluster will be destroyed
  - resource "google_container_cluster" "cluster" {
      - additional_zones          = [
          - "us-central1-b",
          - "us-central1-c",
          - "us-central1-f",
        ] -> null
      - cluster_autoscaling       = [] -> null
      - cluster_ipv4_cidr         = "10.20.0.0/14" -> null
      - default_max_pods_per_node = 110 -> null
      - enable_kubernetes_alpha   = false -> null
      - enable_legacy_abac        = false -> null
      - endpoint                  = "35.225.76.157" -> null
      - id                        = "verbose-equals-true-cluster" -> null
      - initial_node_count        = 1 -> null
      - instance_group_urls       = [
          - "https://www.googleapis.com/compute/v1/projects/verbose-equals-true/zones/us-central1-b/instanceGroups/gke-verbose-equals-t-verbose-equals-t-dee69f6e-grp",
          - "https://www.googleapis.com/compute/v1/projects/verbose-equals-true/zones/us-central1-c/instanceGroups/gke-verbose-equals-t-verbose-equals-t-379740c0-grp",
          - "https://www.googleapis.com/compute/v1/projects/verbose-equals-true/zones/us-central1-f/instanceGroups/gke-verbose-equals-t-verbose-equals-t-0604b9f8-grp",
        ] -> null
      - ip_allocation_policy      = [] -> null
      - location                  = "us-central1" -> null
      - logging_service           = "logging.googleapis.com" -> null
      - master_version            = "1.13.10-gke.0" -> null
      - monitoring_service        = "monitoring.googleapis.com" -> null
      - name                      = "verbose-equals-true-cluster" -> null
      - network                   = "projects/verbose-equals-true/global/networks/default" -> null
      - node_locations            = [
          - "us-central1-b",
          - "us-central1-c",
          - "us-central1-f",
        ] -> null
      - node_version              = "1.13.10-gke.0" -> null
      - project                   = "verbose-equals-true" -> null
      - region                    = "us-central1" -> null
      - remove_default_node_pool  = true -> null
      - resource_labels           = {} -> null
      - services_ipv4_cidr        = "10.23.240.0/20" -> null
      - subnetwork                = "projects/verbose-equals-true/regions/us-central1/subnetworks/default" -> null

      - addons_config {

          - kubernetes_dashboard {
              - disabled = true -> null
            }

          - network_policy_config {
              - disabled = false -> null
            }
        }

      - master_auth {
          - cluster_ca_certificate = "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURDekNDQWZPZ0F3SUJBZ0lRZTF1SXNuTTR6YndYNjg0Z2JxazRvakFOQmdrcWhraUc5dzBCQVFzRkFEQXYKTVMwd0t3WURWUVFERXlRek5tRXhNekpsTXkxaE1HUmxMVFJsWVRNdE9UQmpNaTFqWW1Wak56SmlaamsyTkdZdwpIaGNOTVRreE1ERXpNak14TXpBeVdoY05NalF4TURFeU1EQXhNekF5V2pBdk1TMHdLd1lEVlFRREV5UXpObUV4Ck16SmxNeTFoTUdSbExUUmxZVE10T1RCak1pMWpZbVZqTnpKaVpqazJOR1l3Z2dFaU1BMEdDU3FHU0liM0RRRUIKQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUURQbFZvVjR4d0lqbHprRlFiQ3p1NDFhbEN0SVE4UFh5ekpmeUwyRkk4VApHQVJpZGQwTWlTb05NY3Z3aXZIVk1xei9rTFdNa2RjWjJvVW9Qc0ZOZjY0ZGJ3VU9OOWRFN2Z4Q0k5K0tzUUlHCk1kckVkM2dKd0F3WFVGQSthMXpRVHBVZVJiQTFZQTAyVmJnOXh2SVZuQjJ4N3VpYW0vVWxSQnl1Ly9ubi9MN3YKdjF0RlBEUFdwV1YyaTRMa0xFM3dPaVJaVkJJZy8rU0ozNTVxMnlnVEloVmRaUHBkdHJBWEJWbG5qRFp6OUYzYwo5Zk8veVExWGQrazEva1RLR3hSVmhvMG1HZkFNS011Z0VWSEZJV2lIME9Rc3ByZHI3Wjk3T1FPaVRxY2RPcmg0CitObUZsSWd1c01Cb2gyV2JEVVEvb1ZCeks3OFg3ZThOWTJkSTFVWks1RnR0QWdNQkFBR2pUQURBUUgvTUEwR0NTcUdTSWIzRFFFQkN3VUFBNElCQVFBeApLRGM4OW5BN21ab2R2bHhhemNCKzdtRFpkZHgyVVkzT0NrY3V2RzZKcUJjVmtEUXRCRk9ReEhNeGMwcm12enpKCkQyUVoxME1Hd3M0Mkt0akRLcGl0Qm5SNHJCRGMyZ1hJdVQ4UzdOWlpXaEJVOHdNeDFjYkJUK0JhQ2J1UlpNZk0KVzlhUWNQWUM3aXJaNE1TaVhRWFNPYk00SFBHL3Y0YkcrWUFyVHdFT1MwVjF6QlFOTFFxeTJXZ3Zqc2dnY09MdQpUY0pUY01tSFlCM241NVE5emh1NUc0QThHY1ZWTldKS2lXN3Q5aGZXeDgvclN3aDdNUElqZWFJQWd6VU9UZjM2CmJLdkhsaS9sTUhNamd2M0lxMlFKUlduVkNkUFRWbjhjMkFxbGtjS05HRGRsRmVvaHlDWmV2MTBPV21jdmx1eDkKOERRQWkzRHJkMHc3QVllQjI2WHAKLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=" -> null

          - client_certificate_config {
              - issue_client_certificate = false -> null
            }
        }

      - network_policy {
          - enabled  = true -> null
          - provider = "CALICO" -> null
        }

      - node_config {
          - disk_size_gb      = 100 -> null
          - disk_type         = "pd-standard" -> null
          - guest_accelerator = [] -> null
          - image_type        = "COS" -> null
          - labels            = {} -> null
          - local_ssd_count   = 0 -> null
          - machine_type      = "n1-standard-1" -> null
          - metadata          = {
              - "disable-legacy-endpoints" = "true"
            } -> null
          - oauth_scopes      = [
              - "https://www.googleapis.com/auth/devstorage.read_only",
              - "https://www.googleapis.com/auth/logging.write",
              - "https://www.googleapis.com/auth/monitoring",
            ] -> null
          - preemptible       = false -> null
          - service_account   = "default" -> null
          - tags              = [] -> null
        }

      - node_pool {
          - initial_node_count  = 1 -> null
          - instance_group_urls = [
              - "https://www.googleapis.com/compute/v1/projects/verbose-equals-true/zones/us-central1-b/instanceGroupManagers/gke-verbose-equals-t-verbose-equals-t-dee69f6e-grp",
              - "https://www.googleapis.com/compute/v1/projects/verbose-equals-true/zones/us-central1-c/instanceGroupManagers/gke-verbose-equals-t-verbose-equals-t-379740c0-grp",
              - "https://www.googleapis.com/compute/v1/projects/verbose-equals-true/zones/us-central1-f/instanceGroupManagers/gke-verbose-equals-t-verbose-equals-t-0604b9f8-grp",
            ] -> null
          - max_pods_per_node   = 0 -> null
          - name                = "verbose-equals-true-general" -> null
          - node_count          = 1 -> null
          - version             = "1.13.10-gke.0" -> null

          - autoscaling {
              - max_node_count = 1 -> null
              - min_node_count = 1 -> null
            }

          - management {
              - auto_repair  = true -> null
              - auto_upgrade = true -> null
            }

          - node_config {
              - disk_size_gb      = 100 -> null
              - disk_type         = "pd-standard" -> null
              - guest_accelerator = [] -> null
              - image_type        = "COS" -> null
              - labels            = {} -> null
              - local_ssd_count   = 0 -> null
              - machine_type      = "n1-standard-1" -> null
              - metadata          = {
                  - "disable-legacy-endpoints" = "true"
                } -> null
              - oauth_scopes      = [
                  - "https://www.googleapis.com/auth/devstorage.read_only",
                  - "https://www.googleapis.com/auth/logging.write",
                  - "https://www.googleapis.com/auth/monitoring",
                ] -> null
              - preemptible       = false -> null
              - service_account   = "default" -> null
              - tags              = [] -> null
            }
        }
    }

  # google_container_node_pool.general_purpose will be destroyed
  - resource "google_container_node_pool" "general_purpose" {
      - cluster             = "verbose-equals-true-cluster" -> null
      - id                  = "us-central1/verbose-equals-true-cluster/verbose-equals-true-general" -> null
      - initial_node_count  = 1 -> null
      - instance_group_urls = [
          - "https://www.googleapis.com/compute/v1/projects/verbose-equals-true/zones/us-central1-b/instanceGroupManagers/gke-verbose-equals-t-verbose-equals-t-dee69f6e-grp",
          - "https://www.googleapis.com/compute/v1/projects/verbose-equals-true/zones/us-central1-c/instanceGroupManagers/gke-verbose-equals-t-verbose-equals-t-379740c0-grp",
          - "https://www.googleapis.com/compute/v1/projects/verbose-equals-true/zones/us-central1-f/instanceGroupManagers/gke-verbose-equals-t-verbose-equals-t-0604b9f8-grp",
        ] -> null
      - location            = "us-central1" -> null
      - name                = "verbose-equals-true-general" -> null
      - node_count          = 1 -> null
      - project             = "verbose-equals-true" -> null
      - region              = "us-central1" -> null
      - version             = "1.13.10-gke.0" -> null

      - autoscaling {
          - max_node_count = 1 -> null
          - min_node_count = 1 -> null
        }

      - management {
          - auto_repair  = true -> null
          - auto_upgrade = true -> null
        }

      - node_config {
          - disk_size_gb      = 100 -> null
          - disk_type         = "pd-standard" -> null
          - guest_accelerator = [] -> null
          - image_type        = "COS" -> null
          - labels            = {} -> null
          - local_ssd_count   = 0 -> null
          - machine_type      = "n1-standard-1" -> null
          - metadata          = {
              - "disable-legacy-endpoints" = "true"
            } -> null
          - oauth_scopes      = [
              - "https://www.googleapis.com/auth/devstorage.read_only",
              - "https://www.googleapis.com/auth/logging.write",
              - "https://www.googleapis.com/auth/monitoring",
            ] -> null
          - preemptible       = false -> null
          - service_account   = "default" -> null
          - tags              = [] -> null
        }
    }

Plan: 0 to add, 0 to change, 2 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

...
google_container_node_pool.general_purpose: Still destroying... [id=us-central1/verbose-equals-true-cluster/verbose-equals-true-general, 6m30s elapsed]
google_container_node_pool.general_purpose: Still destroying... [id=us-central1/verbose-equals-true-cluster/verbose-equals-true-general, 6m40s elapsed]
google_container_node_pool.general_purpose: Destruction complete after 6m47s
google_container_cluster.cluster: Destroying... [id=verbose-equals-true-cluster]
google_container_cluster.cluster: Still destroying... [id=verbose-equals-true-cluster, 10s elapsed]
...
google_container_cluster.cluster: Still destroying... [id=verbose-equals-true-cluster, 4m0s elapsed]
google_container_cluster.cluster: Still destroying... [id=verbose-equals-true-cluster, 4m10s elapsed]
google_container_cluster.cluster: Still destroying... [id=verbose-equals-true-cluster, 4m20s elapsed]
google_container_cluster.cluster: Still destroying... [id=verbose-equals-true-cluster, 4m30s elapsed]
google_container_cluster.cluster: Destruction complete after 4m37s

Destroy complete! Resources: 2 destroyed.
```

Now let's check on the Persistent Disks:

```
gcloud compute disks list
NAME                                                             LOCATION       LOCATION_SCOPE  SIZE_GB  TYPE         STATUS
gke-verbose-equals-tru-pvc-2b60b760-ee20-11e9-afd8-42010a800fe4  us-central1-c  zone            8        pd-standard  READY
gke-verbose-equals-tru-pvc-0b603b57-ee20-11e9-afd8-42010a800fe4  us-central1-b  zone            8        pd-standard  READY
gke-verbose-equals-tru-pvc-0b6f922a-ee20-11e9-afd8-42010a800fe4  us-central1-f  zone            8        pd-standard  READY
```

Let's delete these with:

```
gcloud compute disks delete `gcloud compute disks list --format='json' | jq '.[] | .name'`
The following disks will be deleted:
 - ["gke-verbose-equals-tru-pvc-0b603b57-ee20-11e9-afd8-42010a800fe4"]
 in [us-east1-b]
 - ["gke-verbose-equals-tru-pvc-0b6f922a-ee20-11e9-afd8-42010a800fe4"]
 in [us-east1-b]
 - ["gke-verbose-equals-tru-pvc-2b60b760-ee20-11e9-afd8-42010a800fe4"]
 in [us-east1-b]

Do you want to continue (Y/n)?
```

::: warning This is not working
The resources were not found
:::


### Deploying to Terraform from GitLab CI

Now that we can deploy Terraform resources from the command line, let's automate this in our GitLab CI pipeline.

First, we need to save our `account.json` file in our GitLab CI variables. This can be done with the following commands:

```
cat terraform/account.json | base64 -w0
```

Save the output of this command to a GitLab CI environment variable called `GCP_SERVICE_ACCOUNT`.


Next we need to define Terraform jobs that will be triggered in our GitLab CI pipeline.

[This link](https://medium.com/@timhberry/terraform-pipelines-in-gitlab-415b9d842596) provides a good introduction to Terraform pipelines in GitLab CI. The examples provided below are based on the techniques described in this article.

[This article](https://learn.hashicorp.com/terraform/development/running-terraform-in-automation) in the Terraform documentation goes into more detail about running Terraform jobs in automated pipelines.

We will start with two pipelines: `Terraform Plan` and `Terraform Apply`.

::: tip GitLab CI modules
The following example can be found in `/gitlab-ci/gcp.yml`. This file is referenced in the main `.gitlab-ci.yml` file. This will
:::

```yml
Terraform Plan: &terraform
  stage: plan
  image:
    name: hashicorp/terraform:light
    entrypoint:
      - '/usr/bin/env'
      - 'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
  before_script:
    - cd terraform
    - echo $GCP_SERVICE_ACCOUNT | base64 -d > ./account.json
    - terraform init -var-file=production.tfvars
  script:
    - terraform plan -out "planfile" -var-file=production.tfvars
  artifacts:
    paths:
      - terraform/planfile

Terraform Apply:
  <<: *terraform
  stage: deploy
  dependencies:
    - "Terraform Plan"
  script:
    - terraform apply -input=false "planfile"
  when: manual
  artifacts: {}
```


::: warning In progress
This section is not complete. Updates coming soon.
:::
