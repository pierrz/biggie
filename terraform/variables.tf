# Scaleway provider variables
variable "scaleway_access_key" {
  description = "Scaleway access key"
  type        = string
}
variable "scaleway_secret_key" {
  description = "Scaleway secret key"
  type        = string
}
variable "scaleway_organization_id" {
  description = "Scaleway organization ID"
  type        = string
}
variable "scaleway_project_id" {
  description = "Scaleway project ID."
  type        = string
}
variable "scaleway_zone" {
  description = "Scaleway zone"
  type        = string
}
variable "scaleway_server_name" {
  description = "The Scaleway server name"
  type        = string
}
variable "scaleway_server_id" {
  description = "The Scaleway server ID"
  type        = string
}
variable "scaleway_server_os_id" {
  description = "The Scaleway server name"
  type        = string
}
variable "scaleway_server_public_ip" {
  description = "The Scaleway server name"
  type        = string
}
variable "scaleway_server_user" {
  description = "The user used to connect to server"
  type        = string
}
# TODO: improve the key property management to avoid warnings
variable "scaleway_ssh_key_names" {
  description = "The ssh key names from the Scaleway server"
  type        = string
}


# Teleport variables
variable "teleport_proxy" {
  description = "Teleport proxy URL"
  type        = string
}
variable "teleport_bot" {
  description = "Teleport bot name, used as token variable in the action"
  type        = string
}


# Github variables
variable "github_workspace" {
  description = "Root directory of the GitHub workspace"
  type        = string
}
variable "github_repo_name" {
  description = "Name of the GitHub repository"
  type        = string
}
variable "github_repo_branch" {
  description = "Branch currently in use with the GitHub repository"
  type        = string
}


# Docker routing variables
variable "docker_subnet_base" {
  description = "Docker subnet base"
  type        = string
}
variable "compose_prefix" {
  description = "Compose prefix used to name containers and volumes"
  type        = string
}
variable "spark_ports_range" {
  description = "Prefix used to change the range of Spark ports"
  type        = number
}
variable "rabbitmq_port" {
  description = "RabbitMQ port"
  type        = number
}
variable "logs_dir" {
  description = "Logs directory path"
  type        = string
}
variable "data_dir" {
  description = "Data directory path"
  type        = string
}
variable "celery_broker_url" {
  description = "Celery broker URL"
  type        = string
}
variable "celery_result_backend" {
  description = "Celery result backend"
  type        = string
}


# DBs variables
variable "db_name" {
  description = "Database name; Used by both PostgresSQL and MongoDB"
  type        = string
}
# Postgres variables
variable "postgres_db" {
  description = "PostgreSQL database for initialization/admin"
  type        = string
}
variable "postgres_user" {
  description = "PostgreSQL user for initialization/admin"
  type        = string
}
variable "postgres_password" {
  description = "PostgreSQL password for initialization/admin"
  type        = string
}
variable "postgres_app_user" {
  description = "PostgreSQL user for clients"
  type        = string
}
variable "postgres_app_password" {
  description = "PostgreSQL password for clients"
  type        = string
}
variable "postgres_port" {
  description = "Host port for PostgreSQL"
  type        = number
}
# Mongo variables
variable "mongo_initdb_root_username" {
  description = "MongoDB username for initialization"
  type        = string
}
variable "mongo_initdb_root_password" {
  description = "MongoDB password for initialization"
  type        = string
}
variable "mongo_username" {
  description = "MongoDB username for clients"
  type        = string
}
variable "mongo_password" {
  description = "MongoDB password for clients"
  type        = string
}
variable "mongo_port" {
  description = "Host port for MongoDB"
  type        = number
}


# Orchestrator variables
variable "token_github_api" {
  description = "GitHub API token"
  type        = string
}
# API variables
variable "api_port" {
  description = "Host port for the API"
  type        = number
}
# Jupyter variables
variable "jupyter_password" {
  description = "Password for Jupyter"
  type        = string
}
variable "jupyter_port" {
  description = "Host port for the Jupyter"
  type        = number
}


# Monitoring
# Flower variables
variable "flower_port" {
  description = "Host port for FLower"
  type        = number
}
# DBeaver variables
variable "dbeaver_port" {
  description = "Host port for DBeaver"
  type        = number
}
# Mongo-Express variables
variable "me_config_mongodb_adminusername" {
  description = "Admin username for Mongo Express"
  type        = string
}

variable "me_config_mongodb_adminpassword" {
  description = "Admin password for Mongo Express"
  type        = string
}

variable "me_config_basicauth_username" {
  description = "Basic auth username for Mongo Express"
  type        = string
}

variable "me_config_basicauth_password" {
  description = "Basic auth password for Mongo Express"
  type        = string
}
variable "me_config_port" {
  description = "Host port for Mongo Express"
  type        = number
}
