resource "digitalocean_container_registry" "masters_degree" {
  name                   = "masters-degree"
  subscription_tier_slug = "basic"
  region                 = "fra1"
}
