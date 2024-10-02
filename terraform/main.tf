provider "scaleway" {
    access_key = var.scaleway_access_key
    secret_key = var.scaleway_secret_key
    organization_id = var.scaleway_organization_id
    region = "fr-par"
}

resource "scaleway_instance_server" "horseradish" {
    name  = "horseradish"
    type  = "DEV1-S"
    image = "ubuntu_focal"

    tags = ["dummy-test"]

    connection {
        type     = "ssh"
        user     = "terraform"
        password = var.server_password
        host     = self.public_ip
    }

    # Dummy Provisioner
    provisioner "remote-exec" {
        inline = [
            "echo 'Terraform CD Test' > /tmp/terraform_cd_test.txt"
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

# variable "scaleway_access_key" {
#     description = "Scaleway access key"
#     type        = string
# }

# variable "scaleway_secret_key" {
#     description = "Scaleway secret key"
#     type        = string
# }

# variable "scaleway_organization_id" {
#     description = "Scaleway organization ID"
#     type        = string
# }

# variable "server_password" {
#     description = "The password for the server"
#     type        = string
# }
