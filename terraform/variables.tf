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
  type        = number
  description = "Prefix used to change the range of Spark ports"
}
variable "rabbitmq_port" {
  type        = number
  description = "RabbitMQ port"
}
variable "logs_dir" {
  type        = string
  description = "Logs directory path"
}
variable "data_dir" {
  type        = string
  description = "Data directory path"
}


# DBs variables
variable "db_name" {
  type        = string
  description = "Database name; Used by both PostgresSQL and MongoDB"
}
# Postgres variables
variable "postgres_db" {
  type        = string
  description = "PostgreSQL database for initialization/admin"
}
variable "postgres_user" {
  type        = string
  description = "PostgreSQL user for initialization/admin"
}
variable "postgres_password" {
  type        = string
  description = "PostgreSQL password for initialization/admin"
}
variable "postgres_app_user" {
  type        = string
  description = "PostgreSQL user for clients"
}
variable "postgres_app_password" {
  type        = string
  description = "PostgreSQL password for clients"
}
variable "postgres_port" {
  type        = number
  description = "Host port for PostgreSQL"
}
# Mongo variables
variable "mongo_initdb_root_username" {
  type        = string
  description = "MongoDB username for initialization"
}
variable "mongo_initdb_root_password" {
  type        = string
  description = "MongoDB password for initialization"
}
variable "mongo_username" {
  type        = string
  description = "MongoDB username for clients"
}
variable "mongo_password" {
  type        = string
  description = "MongoDB password for clients"
}


# Orchestrator variables
variable "celery_broker_url" {
  type        = string
  description = "Celery broker URL"
}
variable "celery_result_backend" {
  type        = string
  description = "Celery result backend"
}
variable "token_github_api" {
  type        = string
  description = "GitHub API token"
}


# Monitoring
# Flower variables
variable "flower_port" {
  description = "Host port for FLower"
  type        = number
}
# PGAdmin variables
variable "pgadmin_default_email" {
  description = "Default email for pgAdmin"
  type        = string
}
variable "pgadmin_default_password" {
  description = "Default password for pgAdmin"
  type        = string
}
variable "pgadmin_default_port" {
  description = "Host port for pgAdmin"
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
