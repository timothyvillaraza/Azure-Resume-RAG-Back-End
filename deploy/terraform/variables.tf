variable "postgres_admin_username" {
  description = "The administrator username for the PostgreSQL server"
  type        = string
  default     = "pgadmin"  # Optional: you can provide a default value or leave it to be set in the secrets file
}

variable "postgres_admin_password" {
  description = "The password for the PostgreSQL server administrator"
  type        = string
  sensitive   = true
}