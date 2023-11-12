resource "digitalocean_kubernetes_cluster" "masters-degree" {
  name     = "masters-degree-doks"
  region   = "fra1"
  vpc_uuid = digitalocean_vpc.masters_degree.id

  version = "1.28.2-do.0"

  registry_integration = true

  node_pool {
    name       = "autoscale-worker-pool"
    size       = "s-1vcpu-2gb"
    auto_scale = true
    min_nodes  = 1
    max_nodes  = 3
  }
}
