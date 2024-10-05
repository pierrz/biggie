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

  # if [[ "${var.github_is_pr}" == "true" ]]; then
  #   # Fetch the PR and checkout
  #   PULL_NUMBER=${substr(var.github_repo_branch, 6, length(var.github_repo_branch) - 6)}
  #   echo "Pull #$PULL_NUMBER"
  #   git clone git@github.com:${var.github_repo_name}.git /opt/biggie
  #   git fetch origin pull/$PULL_NUMBER/head:pr-$PULL_NUMBER
  #   git checkout pr-$PULL_NUMBER
  # else
  #   # Checkout the regular branch
  #   git clone --branch ${var.github_repo_branch} --single-branch git@github.com:${var.github_repo_name}.git /opt/biggie
  # fi
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
      '
        rm -rf /opt/biggie/.*
        rm -rf /opt/biggie/*
        eval "$(ssh-agent -s)"
        ssh-add /home/terraform-cd/.ssh/id_ed25519_github
        echo "Cloning repository ${var.github_repo_name} on branch ${var.github_repo_branch} ..."
        git clone --branch ${var.github_repo_branch} --single-branch git@github.com:${var.github_repo_name}.git /opt/biggie
        cd /opt/biggie

        echo "Creating .env file ..."
        echo "# main secrets" >> .env
        echo "CELERY_BROKER_URL=${var.celery_broker_url}" >> .env
        echo "CELERY_RESULT_BACKEND=${var.celery_result_backend}" >> .env
        echo "DB_NAME=${var.db_name}" >> .env
        echo "POSTGRES_DB=${var.postgres_db}" >> .env
        echo "POSTGRES_USER=${var.postgres_user}" >> .env
        echo "POSTGRES_PASSWORD=${var.postgres_password}" >> .env
        echo "DB_USER=${var.db_user}" >> .env
        echo "DB_PASSWORD=${var.db_password}" >> .env
        echo "MONGODB_URI=${var.mongodb_uri}" >> .env
        echo "MONGO_INITDB_ROOT_USERNAME=${var.mongo_initdb_root_username}" >> .env
        echo "MONGO_INITDB_ROOT_PASSWORD=${var.mongo_initdb_root_password}" >> .env
        echo "TOKEN_GITHUB_API=${var.token_github_api}" >> .env
        echo "DATA_DIR=${var.data_dir}" >> .env
        echo "LOGS_DIR=${var.logs_dir}" >> .env
        echo "DOCKER_SUBNET_BASE=${var.docker_subnet_base}" >> .env
        echo "# monitoring" >> .env
        echo "PGADMIN_DEFAULT_EMAIL=${var.pgadmin_default_email}" >> .env
        echo "PGADMIN_DEFAULT_PASSWORD=${var.pgadmin_default_password}" >> .env
        echo "ME_CONFIG_MONGODB_ADMINUSERNAME=${var.me_config_mongodb_adminusername}" >> .env
        echo "ME_CONFIG_MONGODB_ADMINPASSWORD=${var.me_config_mongodb_adminpassword}" >> .env
        echo "ME_CONFIG_BASICAUTH_USERNAME=${var.me_config_basicauth_username}" >> .env
        echo "ME_CONFIG_BASICAUTH_PASSWORD=${var.me_config_basicauth_password}" >> .env

        echo "Start Docker Compose setup ..."
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
