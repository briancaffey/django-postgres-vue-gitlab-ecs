variable "general_purpose_machine_type" {
  type = "string"
  description = "Machine type to use for the general-purpose node pool. See https://cloud.google.com/compute/docs/machine-types"
}

variable "general_purpose_min_node_count" {
  type = "string"
  description = "The minimum number of nodes PER ZONE in the general-purpose node pool"
  default = 1
}

variable "general_purpose_max_node_count" {
  type = "string"
  description = "The maximum number of nodes PER ZONE in the general-purpose node pool"
  default = 5
}

variable "worker_node_count" {
  type = "string"
  description = "The number of worker nodes to use in the node pool"
  default = 1
}

resource "google_container_cluster" "cluster" {
  name     = "${var.project}-cluster"
  location = "${var.region}"

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count = 1

  # Setting an empty username and password explicitly disables basic auth
  master_auth {
    username = ""
    password = ""
  }

  addons_config {
    network_policy_config {
      disabled = "false"
    }
  }

  network_policy {
    enabled = "true"
    provider = "CALICO"
  }
}

resource "google_container_node_pool" "general_purpose" {
  name       = "${var.project}-general"
  location   = "${var.region}"
  cluster    = "${google_container_cluster.cluster.name}"
  node_count = "${var.worker_node_count}"

  management {
    auto_repair = "true"
    auto_upgrade = "true"
  }

#   autoscaling {
#     min_node_count = "${var.general_purpose_min_node_count}"
#     max_node_count = "${var.general_purpose_max_node_count}"
#   }
  initial_node_count = "${var.general_purpose_min_node_count}"

  node_config {
    machine_type = "${var.general_purpose_machine_type}"

    metadata = {
      disable-legacy-endpoints = "true"
    }


    # Needed for correctly functioning cluster, see
    # https://www.terraform.io/docs/providers/google/r/container_cluster.html#oauth_scopes
    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/devstorage.read_only"
    ]
  }
}

# The following outputs allow authentication and connectivity to the GKE Cluster
# by using certificate-based authentication.
output "client_certificate" {
  value = "${google_container_cluster.cluster.master_auth.0.client_certificate}"
}

output "client_key" {
  value = "${google_container_cluster.cluster.master_auth.0.client_key}"
}

output "cluster_ca_certificate" {
  value = "${google_container_cluster.cluster.master_auth.0.cluster_ca_certificate}"
}
