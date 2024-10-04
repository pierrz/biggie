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

  # Provisioner for MongoDB
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
        '
        sudo apt-get update
        sudo apt-get install -y gnupg
        wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
        echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
        sudo apt-get update
        sudo apt-get install -y mongodb-org=7.0.14 mongodb-org-server=7.0.14 mongodb-org-shell=7.0.14 mongodb-org-mongos=7.0.14 mongodb-org-tools=7.0.14
        sudo systemctl start mongod
        sudo systemctl enable mongod

        # Set up root user with environment variables
        MONGO_INITDB_ROOT_USERNAME=${var.mongo_initdb_root_username}
        MONGO_INITDB_ROOT_PASSWORD=${var.mongo_initdb_root_password}

        # Wait for MongoDB to start
        until mongo --eval "print('MongoDB is ready!')" >/dev/null 2>&1; do
          sleep 1
        done

        # Create admin user
        mongo <<EOF
        use admin
        db.createUser({
          user: "${MONGO_INITDB_ROOT_USERNAME}",
          pwd: "${MONGO_INITDB_ROOT_PASSWORD}",
          roles: [{ role: "root", db: "admin" }]
        })
        EOF

        echo "MongoDB 7.0.14 installation and root user creation completed successfully"
        '
    EOT
  }

  # Provisioner for Mongo-Express
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
        '
        sudo apt-get update
        sudo apt-get install -y nodejs npm  # Install Node.js and npm
        sudo npm install -g mongo-express@1.0.2-20  # Install specific version of Mongo Express globally

        # Set up environment variables for Mongo Express
        echo "ME_CONFIG_MONGODB_ADMINUSERNAME=${var.me_config_mongodb_adminusername}" | sudo tee -a /etc/environment
        echo "ME_CONFIG_MONGODB_ADMINPASSWORD=${var.me_config_mongodb_adminpassword}" | sudo tee -a /etc/environment
        echo "ME_CONFIG_MONGODB_URL=${var.me_config_mongodb_url}" | sudo tee -a /etc/environment

        # Start Mongo Express (run as a background service using nohup)
        nohup mongo-express > /dev/null 2>&1 &

        echo "MongoDB 7.0.14 and Mongo Express 1.0.2-20 installation completed successfully"
        '
    EOT
  }

  # Provisioner for PostgreSQL
  provisioner "file_init-postgres" {
    source      = file("${var.github_workspace}/db/postgres/docker-entrypoint-inidb.d/init-postgres.sh")
    destination = "/tmp/init-postgres.sh"
  }
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
        '
        sudo apt-get update
        sudo apt-get install -y wget gnupg2  # Install wget and gnupg2
        wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
        echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
        sudo apt-get update
        sudo apt-get install -y postgresql-14.9  # Install PostgreSQL 14.9
        sudo systemctl enable postgresql  # Enable PostgreSQL to start on boot
        sudo systemctl start postgresql  # Start PostgreSQL service
        "chmod +x /tmp/init-postgres.sh"
        "sudo POSTGRES_USER=${var.postgres_user} POSTGRES_DB=${var.postgres_db} DB_USER=${var.db_user} DB_PASSWORD=${var.db_password} DB_NAME=${var.db_name} /tmp/init-postgres.sh"
        '
    EOT
  }

  # Provisioner for PGAdmin
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
        '
        sudo apt-get update
        sudo apt-get install -y wget curl ca-certificates gnupg  # Install wget, curl, and gnupg
        curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add -  # Add pgAdmin repository key
        echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" | sudo tee /etc/apt/sources.list.d/pgadmin4.list  # Add pgAdmin repository
        sudo apt-get update
        sudo apt-get install -y pgadmin4-web  # Install pgAdmin
        sudo /usr/pgadmin4/bin/setup-web.sh --yes  # Set up pgAdmin web mode
        sudo sed -i "s/PGADMIN_DEFAULT_EMAIL=.*/PGADMIN_DEFAULT_EMAIL=${var.pgadmin_default_email}/" /etc/pgadmin4/config_local.py  # Set pgAdmin default email
        sudo sed -i "s/PGADMIN_DEFAULT_PASSWORD=.*/PGADMIN_DEFAULT_PASSWORD=${var.pgadmin_default_password}/" /etc/pgadmin4/config_local.py  # Set pgAdmin default password
        sudo systemctl restart apache2  # Restart Apache to apply changes
        echo "pgAdmin 4 installation completed successfully"
        '
    EOT
  }

  # Provisioner for installing pyenv and Python 3.11
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
        '
        sudo apt-get update
        sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
        curl https://pyenv.run | bash
        export PATH="$HOME/.pyenv/bin:$PATH"
        eval "$(pyenv init --path)"
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"
        pyenv install 3.11.9
        pyenv rehash
        '
    EOT
  }

  # Provisioners for the Orchestrator based on Celery
  # provisioner "file_orchestrator-toml" {
  #   source      = file("${var.github_workspace}/orchestrator/pyproject.toml")
  #   destination = "/opt/biggie/orchestrator/pyproject.toml"
  # }
  # provisioner "file_orchestrator-lock" {
  #   source      = file("${var.github_workspace}/orchestrator/poetry.lock")
  #   destination = "/opt/biggie/orchestrator/poetry.lock"
  # }
  provisioner "file_orchestrator_directory" {
    source      = "${var.github_workspace}/orchestrator"
    destination = "/opt/biggie/orchestrator"
    type        = "directory"
  }
  provisioner "file_orchestrator_db" {
    source      = "${var.github_workspace}/db"
    destination = "/opt/biggie/orchestrator/src/db"
    type        = "directory"
  }
  provisioner "file_orchestrator_commons" {
    source      = "${var.github_workspace}/commons"
    destination = "/opt/biggie/orchestrator/src/commons"
    type        = "directory"
  }
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
        '
        sudo mkdir -p /opt/biggie/orchestrator
        apt-get clean && apt-get update && apt-get install -qy openjdk-17-jdk
        export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
        export PYSPARK_HADOOP_VERSION=3
        export PYSPARK_DRIVER_PYTHON=/usr/local/bin/python3.11
        export PYSPARK_PYTHON=/usr/local/bin/python3.11
        export PYTHONFAULTHANDLER=1
        export PYTHONUNBUFFERED=1
        export PYTHONHASHSEED=random
        export PIP_NO_CACHE_DIR=off
        export PIP_DISABLE_PIP_VERSION_CHECK=off
        export PIP_DEFAULT_TIMEOUT=100
        cd /opt/biggie/orchestrator
        pyenv virtualenv 3.11.9 biggie-orchestrator
        pyenv local biggie-orchestrator
        pyenv activate biggie-orchestrator
        pip install --upgrade pip && pip install poetry
        poetry install --no-interaction --no-ansi --only main,security
        poetry install
        pyenv deactivate
        sudo tee /etc/systemd/system/biggie-orchestrator.service > /dev/null <<EOF
        [Unit]
        Description=Orchestrator Service for Biggie
        After=network.target

        [Service]
        User=${var.scaleway_server_user}
        WorkingDirectory=/opt/biggie/orchestrator
        ExecStart=pyenv activate biggie-orchestrator && sh run.sh
        Restart=always

        [Install]
        WantedBy=multi-user.target
        EOF
        sudo systemctl daemon-reload
        sudo systemctl enable biggie-orchestrator
        sudo systemctl start biggie-orchestrator
        '
    EOT
  }

  # Provisioner for Flower
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
        '
        sudo mkdir -p /opt/biggie/flower
        pyenv virtualenv 3.11.9 biggie-flower
        pyenv local biggie-flower
        pyenv activate biggie-flower
        pip install --upgrade pip && pip install flower==2.0.1
        pyenv deactivate
        sudo tee /etc/systemd/system/biggie-flower.service > /dev/null <<EOF
        [Unit]
        Description=Flower Service for Biggie
        After=network.target

        [Service]
        User=${var.scaleway_server_user}
        WorkingDirectory=/opt/biggie/flower
        ExecStart=/home/${var.scaleway_server_user}/.pyenv/versions/3.11.9/envs/biggie_flower/bin/flower
        Restart=always

        [Install]
        WantedBy=multi-user.target
        EOF
        sudo systemctl daemon-reload
        sudo systemctl enable biggie-flower
        sudo systemctl start biggie-flower
        '
    EOT
  }

  # Provisioners for FastAPI
  provisioner "file_api_directory" {
    source      = "${var.github_workspace}/api"
    destination = "/opt/biggie/orchestrator"
    type        = "directory"
  }
  provisioner "file_api_db" {
    source      = "${var.github_workspace}/db"
    destination = "/opt/biggie/api/src/db"
    type        = "directory"
  }
  provisioner "file_api_commons" {
    source      = "${var.github_workspace}/commons"
    destination = "/opt/biggie/api/src/commons"
    type        = "directory"
  }
  provisioner "local-exec" {
    command = <<-EOT
      set -e
      tsh ssh ${var.scaleway_server_user}@${var.scaleway_server_name} \
        '
        export PYTHONFAULTHANDLER=1
        export PYTHONUNBUFFERED=1
        export PYTHONHASHSEED=random
        export PIP_NO_CACHE_DIR=off
        export PIP_DISABLE_PIP_VERSION_CHECK=on
        export PIP_DEFAULT_TIMEOUT=100
        sudo mkdir -p /opt/biggie/api
        cd /opt/biggie/api
        pyenv virtualenv 3.11.9 biggie-api
        pyenv local biggie-api
        pyenv activate biggie-api
        pip install --upgrade pip && pip install poetry
        poetry install --no-interaction --no-ansi --only main,security
        poetry install
        pyenv deactivate
        sudo tee /etc/systemd/system/biggie-api.service > /dev/null <<EOF
        [Unit]
        Description=API Service for Biggie
        After=network.target

        [Service]
        User=${var.scaleway_server_user}
        WorkingDirectory=/opt/biggie/api
        ExecStart=pyenv activate biggie-api && uvicorn main:app --host 0.0.0.0 --reload --log-level info
        Restart=always

        [Install]
        WantedBy=multi-user.target
        EOF
        sudo systemctl daemon-reload
        sudo systemctl enable biggie-api
        sudo systemctl start biggie-api
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
