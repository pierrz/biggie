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

# Other available resources: scaleway_flexible_ip

resource "null_resource" "server_configuration" {
  triggers = {
    always_run = "${timestamp()}"
  }

  # Connection and command over SSH
  # connection {
  #   type        = "ssh"
  #   user        = var.scaleway_server_user
  #   host        = scaleway_baremetal_server.main.ipv4[0].address
  #   private_key = file("${var.github_workspace}/id_key")
  # }
  # provisioner "remote-exec" {
  #   inline = [
  #     "mkdir -p /tmp/terraform_cd_test",
  #     "echo 'Hello' > /tmp/terraform_cd_test/hello-ssh.txt"
  #   ]
  # }

  # Command over TSH
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

  # Provisioner for Spark
  # provisioner "remote-exec" {
  #     inline = [
  #         "sudo apt-get update",
  #         "sudo apt-get install -y openjdk-8-jdk",  # Spark
  #         "wget https://archive.apache.org/dist/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz",
  #         "tar xvf spark-3.0.0-bin-hadoop2.7.tgz",
  #     ]
  # }

}

# Outputs for easy access to server details
output "server_name" {
  value = scaleway_baremetal_server.main.name
}
output "server_public_ip" {
  value = scaleway_baremetal_server.main.ipv4[0].address
}
