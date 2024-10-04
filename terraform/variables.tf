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

variable "scaleway_server_user" {
  description = "The user used to connect to server"
  type        = string
}

variable "scaleway_server_id" {
  description = "The Scaleway server ID"
  type        = string
}

variable "scaleway_server_name" {
  description = "The Scaleway server name"
  type        = string
}

variable "scaleway_server_public_ip" {
  description = "The Scaleway server name"
  type        = string
}

variable "scaleway_server_os_id" {
  description = "The Scaleway server name"
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
  description = "Teleport bot"
  type        = string
}

# Mongo variables
variable "mongo_initdb_root_username" {
  type        = string
  description = "MongoDB root username"
}

variable "mongo_initdb_root_password" {
  type        = string
  description = "MongoDB root password"
}

variable "mongodb_uri" {
  type        = string
  description = "MongoDB URI"
}

# Postgres variables
variable "postgres_db" {
  type        = string
  description = "Postgres database name"
}

variable "postgres_user" {
  type        = string
  description = "Postgres user"
}

variable "postgres_password" {
  type        = string
  description = "Postgres password"
}

variable "db_name" {
  type        = string
  description = "Database name; Also used for MongoDB"
}

variable "db_user" {
  type        = string
  description = "Database user"
}

variable "db_password" {
  type        = string
  description = "Database password"
}

# Orchestrator variables
variable "token_github_api" {
  type        = string
  description = "GitHub API token"
}

variable "celery_broker_url" {
  type        = string
  description = "Celery broker URL"
}

variable "celery_result_backend" {
  type        = string
  description = "Celery result backend"
}

# Spark variables
variable "spark_master" {
  type        = string
  description = "Spark master URL"
}

variable "spark_mode" {
  type        = string
  description = "Spark mode"
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

variable "me_config_mongodb_enable_admin" {
  description = "Enable admin access for Mongo Express"
  type        = bool
  default     = true
}

variable "me_config_mongodb_url" {
  description = "MongoDB URI for Mongo Express"
  type        = string
  # default     = var.mongodb_uri
}

# Common variables
variable "logs_dir" {
  type        = string
  description = "Logs directory path"
}

variable "data_dir" {
  type        = string
  description = "Data directory path"
}
variable "github_workspace" {
  description = "Root directory of the GitHub workspace"
  type        = string
}
variable "docker_subnet_base" {
  description = "Docker subnet base"
  type        = string

}
