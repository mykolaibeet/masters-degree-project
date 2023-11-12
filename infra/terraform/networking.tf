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

resource "digitalocean_loadbalancer" "masters_degree" {
  name      = "masters-degree"
  region    = "fra1"
  vpc_uuid  = digitalocean_vpc.masters_degree.id
  size_unit = 1

  forwarding_rule {
    entry_port     = 443
    entry_protocol = "tcp"

    target_port     = 443
    target_protocol = "tcp"
  }

  healthcheck {
    port     = 443
    protocol = "tcp"
  }

  droplet_tag = "k8s:worker"
}
