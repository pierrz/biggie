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

resource "null_resource" "server_configuration" {
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

  # Provisioners for the whole Compose setup
  # provisioner "file" {
  #   source      = var.github_workspace
  #   destination = "/opt/biggie"
  # }
  # provisioner "local-exec" {
  #   command = <<-EOT
  #   set -e
  #     tsh scp -r ${var.github_workspace} ${var.scaleway_server_user}@${var.scaleway_server_name}:/opt/biggie
  #   EOT
  # }
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name}
      '
        rm -rf /opt/biggie/*
        ssh-add /home/terraform-cd/.ssh/id_ed25519_github.pub
        git clone git@github.com:${var.github_repo_name}.git:${var.github_repo_branch} /opt/biggie

        sudo tee /opt/biggie/.env > /dev/null <<EOF
          # main secrets
          CELERY_BROKER_URL=${var.celery_broker_url}
          CELERY_RESULT_BACKEND=${var.celery_result_backend}
          DB_NAME=${var.db_name}
          POSTGRES_DB=${var.postgres_db}
          POSTGRES_USER=${var.postgres_user}
          POSTGRES_PASSWORD=${var.postgres_password}
          DB_USER=${var.db_user}
          DB_PASSWORD=${var.db_password}
          MONGODB_URI=${var.mongodb_uri}
          MONGO_INITDB_ROOT_USERNAME=${var.mongo_initdb_root_username}
          MONGO_INITDB_ROOT_PASSWORD=${var.mongo_initdb_root_password}
          TOKEN_GITHUB_API=${var.token_github_api}
          DATA_DIR=${var.data_dir}
          LOGS_DIR=${var.logs_dir}
          DOCKER_SUBNET_BASE=${var.docker_subnet_base}

          # monitoring
          PGADMIN_DEFAULT_EMAIL=${var.pgadmin_default_email}
          PGADMIN_DEFAULT_PASSWORD=${var.pgadmin_default_password}
          ME_CONFIG_MONGODB_ADMINUSERNAME=${var.me_config_mongodb_adminusername}
          ME_CONFIG_MONGODB_ADMINPASSWORD=${var.me_config_mongodb_adminpassword}
          ME_CONFIG_BASICAUTH_USERNAME=${var.me_config_basicauth_username}
          ME_CONFIG_BASICAUTH_PASSWORD=${var.me_config_basicauth_password}
        EOF

        cd /opt/biggie
        docker compose -f docker-compose.yml -f docker-compose.monitoring.yml --profile prod_full -d
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
