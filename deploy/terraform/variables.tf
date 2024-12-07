variable "azure_subscription_id" {
  description = "The Azure subscription ID"
  type        = string
  sensitive   = true
}

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

variable "resume_rag_tags" {
  description = "A map of tags to be applied to all resources"
  type        = map(string)
  default = {
    source      = "terraform"
    environment = "portfolio"
  }
}