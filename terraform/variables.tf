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

variable "scaleway_server_password" {
  description = "The password for the user connecting to the server"
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

variable "scaleway_ssh_key_id" {
  description = "The ssh key ID from the Scaleway server"
  type        = string
}
