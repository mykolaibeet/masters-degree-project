terraform {
  cloud {
    organization = "mykolaibeet"

    workspaces {
      name = "masters-degree-project"
    }
  }

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "2.32.0"
    }
  }
}

variable "do_token" {
  type    = string
}

provider "digitalocean" {
  token = var.do_token
}


