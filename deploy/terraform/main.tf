# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.74"
    }
  }
  required_version = ">= 1.3.0"
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "rg_resume_rag" {
  name     = "rgresumerag"
  location = "Central US"

  tags = {
    source      = "terraform"
    environment = "portfolio"
  }
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "pg_resume_rag" {
  name                = "pgresumerag"
  resource_group_name = azurerm_resource_group.rg_resume_rag.name
  location            = azurerm_resource_group.rg_resume_rag.location
  sku_name            = "B_Standard_B1ms"
  storage_mb          = 32768
  version             = "15"
  administrator_login = var.postgres_admin_username
  administrator_password = var.postgres_admin_password

  tags = {
    source      = "terraform"
    environment = "portfolio"
  }
}

# Allow-List the 'vector' Extension
resource "azurerm_postgresql_flexible_server_configuration" "allow_vector_extension" {
  name      = "azure.extensions"
  server_id = azurerm_postgresql_flexible_server.pg_resume_rag.id
  value     = "vector"
}

# PostgreSQL Database
resource "azurerm_postgresql_flexible_server_database" "pgdb_resume_rag" {
  name      = "pgdbresumerag"
  server_id = azurerm_postgresql_flexible_server.pg_resume_rag.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Azure Storage Account
resource "azurerm_storage_account" "storage_account_resume_rag" {
  name                     = "saresumerag"
  resource_group_name      = azurerm_resource_group.rg_resume_rag.name
  location                 = azurerm_resource_group.rg_resume_rag.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    source      = "terraform"
    environment = "portfolio"
  }
}

# Blob Container
resource "azurerm_storage_container" "blob_container_resume_rag" {
  name                  = "bcresumerag"
  storage_account_name  = azurerm_storage_account.storage_account_resume_rag.name
  container_access_type = "private"
}

# Outputs
output "resource_group_name" {
  value = azurerm_resource_group.rg_resume_rag.name
}

output "postgresql_server_name" {
  value = azurerm_postgresql_flexible_server.pg_resume_rag.name
}

output "postgresql_database_name" {
  value = azurerm_postgresql_flexible_server_database.pgdb_resume_rag.name
}

output "storage_account_name" {
  value = azurerm_storage_account.storage_account_resume_rag.name
}

output "blob_container_name" {
  value = azurerm_storage_container.blob_container_resume_rag.name
}