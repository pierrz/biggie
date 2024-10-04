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

variable "github_workspace" {
  description = "Root directory of the GitHub workspace"
  type        = string
}

variable "teleport_proxy" {
  description = "Teleport proxy URL"
  type        = string
}

variable "teleport_bot" {
  description = "Teleport bot"
  type        = string
}
