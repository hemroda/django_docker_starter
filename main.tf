terraform {
  required_version = ">= 0.12"
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "1.46.1"
    }
  }
}

provider "hcloud" {
  token = var.hetzner_cloud_api_token
}

resource "hcloud_firewall" "web_server_and_ssh" {
  name = "Web Server and SSH"

  rule {
    description = "Allow HTTP traffic"
    direction   = "in"
    protocol    = "tcp"
    port        = "80"
    source_ips = [
      "0.0.0.0/0",
      "::/0"
    ]
  }

  rule {
    description = "Allow HTTPS traffic"
    direction   = "in"
    protocol    = "tcp"
    port        = "443"
    source_ips = [
      "0.0.0.0/0",
      "::/0"
    ]
  }

  rule {
    description = "Allow SSH traffic"
    direction   = "in"
    protocol    = "tcp"
    port        = "22"
    source_ips = [
      "0.0.0.0/0",
      "::/0"
    ]
  }
}

data "hcloud_ssh_key" "django_docker_starter_ssh_key" {
  fingerprint = var.hetzner_ssh_key_fingerprint
}

resource "hcloud_network" "django_docker_starter_private_network" {
  name     = "django_docker_starter Private Network"
  ip_range = "10.0.0.0/16"
}

resource "hcloud_network_subnet" "django_docker_starter_private_network_subnet" {
  type         = "cloud"
  network_id   = hcloud_network.django_docker_starter_private_network.id
  network_zone = "eu-central"
  ip_range     = "10.0.1.0/24"
}

resource "hcloud_server" "django_docker_starter" {
  name         = "django_docker_starter"
  server_type  = "cpx21"
  location     = "nbg1"
  image        = "ubuntu-24.04"
  ssh_keys     = [data.hcloud_ssh_key.django_docker_starter_ssh_key.id]
  firewall_ids = [hcloud_firewall.web_server_and_ssh.id]

  network {
    network_id = hcloud_network.django_docker_starter_private_network.id
  }

  depends_on = [
    hcloud_network_subnet.django_docker_starter_private_network_subnet
  ]

  # Pre-install Docker using user_data
  user_data = <<-EOF
              #!/bin/bash
              # Update the package list
              apt-get update

              # Install required packages
              apt-get install -y \
                  ca-certificates \
                  curl \
                  gnupg

              # Add Docker's official GPG key
              install -m 0755 -d /etc/apt/keyrings
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
                  gpg --dearmor -o /etc/apt/keyrings/docker.gpg
              chmod a+r /etc/apt/keyrings/docker.gpg

              # Set up the repository
              echo \
                  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
                  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

              # Install Docker
              apt-get update
              apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

              # Install specific version of docker-compose
              DOCKER_COMPOSE_VERSION="v2.24.5"
              curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

              # Start Docker service
              systemctl start docker
              systemctl enable docker

              # Add user to docker group
              usermod -aG docker ubuntu
              newgrp docker
              EOF
}
