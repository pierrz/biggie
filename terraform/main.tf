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

  # Install repository
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

        echo "Prepare Jupyter hash ..."
        # cd /home/${var.scaleway_server_user}
        # . biggie-cd-venv/bin/activate
        # HASHED_PASSWORD=$(python -c "from jupyter_server.auth import passwd; print(passwd('${var.jupyter_password}'))")
        /home/${var.scaleway_server_user}/biggie-cd-venv/bin/python3 -m pip list
        HASHED_PASSWORD=$(/home/${var.scaleway_server_user}/biggie-cd-venv/bin/python3 -c "from jupyter_server.auth import passwd; print(passwd('${var.jupyter_password}'))")
        echo "$HASHED_PASSWORD"
      '
    EOT
  }

  # Retrieve Jupyter hashed password
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh scp ./hashed_password.txt ${var.scaleway_server_user}@${var.scaleway_server_name}:/opt/biggie
    EOT
  }

  # Prepare .env and run tests
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
      '
        echo "Creating .env file ..."
        cd /opt/biggie

        echo "# Docker routing" >> .env
        echo "DOCKER_SUBNET_BASE=${var.docker_subnet_base}" >> .env
        echo "COMPOSE_PREFIX=${var.compose_prefix}" >> .env
        echo "SPARK_PORTS_RANGE=${var.spark_ports_range}" >> .env
        echo "RABBITMQ_PORT=${var.rabbitmq_port}" >> .env
        echo "DATA_DIR=${var.data_dir}" >> .env
        echo "LOGS_DIR=${var.logs_dir}" >> .env
        echo "CELERY_BROKER_URL=${var.celery_broker_url}" >> .env
        echo "CELERY_RESULT_BACKEND=${var.celery_result_backend}" >> .env
        echo "" >> .env
        echo "# DBs" >> .env
        echo "DB_NAME=${var.db_name}" >> .env
        echo "# PostgresSQL" >> .env
        echo "POSTGRES_DB=${var.postgres_db}" >> .env
        echo "POSTGRES_USER=${var.postgres_user}" >> .env
        echo "POSTGRES_PASSWORD=${var.postgres_password}" >> .env
        echo "POSTGRES_APP_USER=${var.postgres_app_user}" >> .env
        echo "POSTGRES_APP_PASSWORD=${var.postgres_app_password}" >> .env
        echo "POSTGRES_PORT=${var.postgres_port}" >> .env
        echo "# MongoDB" >> .env
        echo "MONGO_INITDB_ROOT_USERNAME=${var.mongo_initdb_root_username}" >> .env
        echo "MONGO_INITDB_ROOT_PASSWORD=${var.mongo_initdb_root_password}" >> .env
        echo "MONGO_USERNAME=${var.mongo_username}" >> .env
        echo "MONGO_PASSWORD=${var.mongo_password}" >> .env
        echo "MONGO_PORT=${var.mongo_port}" >> .env
        echo "" >> .env
        echo "# SERVICES" >> .env
        echo "# Orchestrator" >> .env
        echo "TOKEN_GITHUB_API=${var.token_github_api}" >> .env
        echo "# API" >> .env
        echo "API_PORT=${var.api_port}" >> .env
        echo "# Jupyter" >> .env
        # echo "JUPYTER_HASHED_PASSWORD=$HASHED_PASSWORD" >> .env
        echo "JUPYTER_HASHED_PASSWORD=$(cat ./hashed_password.txt | tr -d '\n')" >> .env
        echo "JUPYTER_PORT=${var.jupyter_port}" >> .env
        echo "" >> .env
        echo "# Monitoring" >> .env
        echo "# Flower" >> .env
        echo "FLOWER_PORT=${var.flower_port}" >> .env
        echo "# DBeaver" >> .env
        echo "DBEAVER_PORT=${var.dbeaver_port}" >> .env
        echo "# Mongo-Express" >> .env
        echo "ME_CONFIG_MONGODB_ADMINUSERNAME=${var.me_config_mongodb_adminusername}" >> .env
        echo "ME_CONFIG_MONGODB_ADMINPASSWORD=${var.me_config_mongodb_adminpassword}" >> .env
        echo "ME_CONFIG_BASICAUTH_USERNAME=${var.me_config_basicauth_username}" >> .env
        echo "ME_CONFIG_BASICAUTH_PASSWORD=${var.me_config_basicauth_password}" >> .env
        echo "ME_CONFIG_PORT=${var.me_config_port}" >> .env

        # echo "Clean Docker components ..."
        # docker network rm biggie_network || true
        # docker container stop $(docker ps --format "{{.Names}}" | grep "^biggie_")
        # docker container rm $(docker ps --format "{{.Names}}" | grep "^biggie_")
        # docker container stop biggie_network || true

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
