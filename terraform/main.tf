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

data "scaleway_account_ssh_key" "existing_keys" {
  name       = "*"
  project_id = var.scaleway_project_id
  # values = ["*"]  # Replace "*" with the desired substring or pattern
}
# data scaleway_account_project "by_id" {
#   project_id = var.scaleway_project_id
# }

resource "scaleway_baremetal_server" "main" {
  name        = var.scaleway_server_name
  offer       = "EM-A115X-SSD"
  tags        = ["muzai.io", "biggie", "teleport", "production"]
  zone        = var.scaleway_zone
  os          = var.scaleway_server_os_id
  ssh_key_ids = [for key in data.scaleway_account_ssh_key.existing_keys : key.id]
  # ssh_key_ids = []
  # ssh_key_ids = [var.scaleway_ssh_key_id]

  # Private network configuration (if applicable)
  # private_network {
  #   id = "your-private-network-id"
  # }

  lifecycle {
    prevent_destroy = true
  }

  # user_data = {
  #   cloud-init = <<-EOF
  #     #cloud-config
  #     package_update: true
  #     package_upgrade: true
  #     packages:
  #       - nginx
  #       - nodejs
  #       - npm
  #     write_files:
  #       - path: /etc/nginx/sites-available/default
  #         content: |
  #           server {
  #             listen 80 default_server;
  #             server_name _;
  #             location / {
  #               proxy_pass http://localhost:3000;
  #               proxy_http_version 1.1;
  #               proxy_set_header Upgrade $http_upgrade;
  #               proxy_set_header Connection 'upgrade';
  #               proxy_set_header Host $host;
  #               proxy_cache_bypass $http_upgrade;
  #             }
  #           }
  #     runcmd:
  #       - systemctl restart nginx
  #       - npm install -g pm2
  #       - git clone https://github.com/your-repo/your-nodejs-app.git /opt/app
  #       - cd /opt/app && npm install
  #       - pm2 start /opt/app/index.js
  #       - pm2 startup systemd
  #       - pm2 save
  #   EOF
  # }

  connection {
    type = "ssh"
    user = var.scaleway_server_user
    # password = var.scaleway_server_password
    host = var.scaleway_server_public_ip
    # host        = scaleway_baremetal_server.main.public_ip
    private_key = file("/tmp/id_key")
  }

  # Dummy Provisioner
  provisioner "remote-exec" {
    inline = [
      "mkdir -p /tmp/terraform_cd_test",
      "echo 'Hello' > /tmp/terraform_cd_test/hello.txt"
    ]
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

# Optionally, manage associated resources like a flexible IP
# resource "scaleway_flexible_ip" "main_ip" {
#   server_id = scaleway_baremetal_server.main.id
#   zone      = var.scaleway_zone
# }

# Outputs for easy access to server details
output "server_id" {
  value = scaleway_baremetal_server.main.id
}

output "server_name" {
  value = scaleway_baremetal_server.main.name
}

output "public_ip" {
  value = scaleway_baremetal_server.main.ips
}
