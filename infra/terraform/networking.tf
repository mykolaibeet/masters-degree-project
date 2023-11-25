resource "digitalocean_vpc" "masters_degree" {
  name     = "masters-degree-vpc"
  region   = "fra1"
  ip_range = "10.100.0.0/16"
}

resource "digitalocean_firewall" "masters_degree_main" {
  name = "masters-degree-main"

  tags = ["k8s:worker"]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0"]
  }
}
