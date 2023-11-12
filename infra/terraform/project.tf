resource "digitalocean_project" "masters_degree" {
  name        = "masters-degree"
  description = "A project to represent university project."
  purpose     = "Education"
  environment = "Development"
  resources   = [digitalocean_kubernetes_cluster.masters-degree.urn, digitalocean_loadbalancer.masters_degree.urn]
}
