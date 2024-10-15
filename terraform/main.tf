# Terraform configuration to import current server
# and install the latest changes from the repository

# Documentation: https://registry.terraform.io/providers/scaleway/scaleway/latest/docs

terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
  required_version = ">= 0.13"
}

provider "scaleway" {
  access_key      = var.scaleway_access_key
  secret_key      = var.scaleway_secret_key
  organization_id = var.scaleway_organization_id
  zone            = var.scaleway_zone
  region          = substr(var.scaleway_zone, 0, 6)
}

# SSH keys from project
# TODO: improve the key property management to avoid warnings
# - why need to fetch these keys?
# - better method?
locals {
  ssh_key_names = split(",", var.scaleway_ssh_key_names)
}
data "scaleway_account_ssh_key" "ssh_key_0" {
  name       = local.ssh_key_names[0]
  project_id = var.scaleway_project_id
}
data "scaleway_account_ssh_key" "ssh_key_1" {
  name       = local.ssh_key_names[1]
  project_id = var.scaleway_project_id
}

resource "scaleway_baremetal_server" "main" {
  name  = var.scaleway_server_name
  offer = "EM-A115X-SSD"
  tags  = ["muzai.io", "biggie", "teleport", "production"]
  zone  = var.scaleway_zone
  os    = var.scaleway_server_os_id
  # ssh_key_ids = []
  ssh_key_ids = [
    data.scaleway_account_ssh_key.ssh_key_0.id,
    data.scaleway_account_ssh_key.ssh_key_1.id
  ]

  lifecycle {
    prevent_destroy = true
  }

}

resource "null_resource" "compose_setup" {
  triggers = {
    always_run = "${timestamp()}"
  }

  # Dummy command over TSH
  provisioner "local-exec" {
    command = <<-EOT
    set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
      '
        mkdir -p /tmp/terraform_cd_test
        echo "Hello" > /tmp/terraform_cd_test/hello-tsh.txt
        echo "Configuration completed successfully"
      '
    EOT
  }

  # Install repo and run tests
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
      '
        echo "Directory preps ..."
        rm -rf /opt/biggie/.*
        rm -rf /opt/biggie/*

        echo "Cloning repository ${var.github_repo_name} on branch ${var.github_repo_branch} ..."
        eval "$(ssh-agent -s)"
        ssh-add /home/terraform-cd/.ssh/id_ed25519_github
        git clone  \
          --branch ${var.github_repo_branch} \
          --single-branch git@github.com:${var.github_repo_name}.git \
          /opt/biggie

        echo "Creating .env file ..."
        cd /opt/biggie
        chmod +x ./terraform/create_env.sh
        ./terraform/create_env.sh

        echo "Clean Docker components ..."
        docker network rm biggie_network || true
        docker container stop $(docker ps --format "{{.Names}}" | grep "^biggie_")
        docker container rm $(docker ps --format "{{.Names}}" | grep "^biggie_")
        docker container stop biggie_network || true

        echo "Test compose setup ..."
        docker compose up api-test orchestrator-test --build
      '
    EOT
  }

  # Run repo in full mode
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
      '
        echo "Run compose setup ..."
        cd /opt/biggie
        docker compose \
          -f compose.yaml \
          -f compose.monitoring.yaml \
          --profile prod_full \
          up --build --detach
      '
    EOT
  }

}

# Outputs for easy access to server details
output "server_name" {
  value = scaleway_baremetal_server.main.name
}
output "server_public_ip" {
  value = scaleway_baremetal_server.main.ipv4[0].address
}
