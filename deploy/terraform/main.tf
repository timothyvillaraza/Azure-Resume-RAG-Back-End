# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.0.0"
    }
  }
  required_version = ">= 1.3.0"
}

# Azure Provider Configuration
provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}

# Resource Group
resource "azurerm_resource_group" "resource_group_resume_rag" {
  name     = "rgresumerag"
  location = "Central US"

  tags = var.resume_rag_tags
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "pg_resume_rag" {
  name                = "pgresumerag"
  resource_group_name = azurerm_resource_group.resource_group_resume_rag.name
  location            = azurerm_resource_group.resource_group_resume_rag.location
  sku_name            = "B_Standard_B1ms"
  storage_mb          = 32768
  version             = "15"
  administrator_login = var.postgres_admin_username
  administrator_password = var.postgres_admin_password
  zone                = "2"            # Auto assigned to 2 by default, now explictly adding to avoid as detected change on rerun
  
  public_network_access_enabled = true # Allows for public access from any Azure service. For our application, it allows other function apps to access the db.

  tags = var.resume_rag_tags
}

# Allows Azure Services - Use Case: Allows function apps to access flexible server dbs 
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure_services" {
  name                = "AllowAzureServices"
  server_id           = azurerm_postgresql_flexible_server.pg_resume_rag.id
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
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
  resource_group_name      = azurerm_resource_group.resource_group_resume_rag.name
  location                 = azurerm_resource_group.resource_group_resume_rag.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = var.resume_rag_tags
}

# Blob Container
resource "azurerm_storage_container" "blob_container_resume_rag" {
  name                  = "bcresumerag"
  storage_account_id  = azurerm_storage_account.storage_account_resume_rag.id
  container_access_type = "private"
}

# App Service Plan
resource "azurerm_service_plan" "app_service_plan_resume_rag" {
  name                = "aspresumerag"
  location            = azurerm_resource_group.resource_group_resume_rag.location
  resource_group_name = azurerm_resource_group.resource_group_resume_rag.name
  os_type             = "Linux"
  sku_name            = "Y1"     # Consumption Plan

  tags = var.resume_rag_tags
}

# Linux Function Apps
resource "azurerm_linux_function_app" "function_app_resume_rag" {
  name                = "faresumerag"
  resource_group_name = azurerm_resource_group.resource_group_resume_rag.name
  location            = azurerm_resource_group.resource_group_resume_rag.location

  storage_account_name       = azurerm_storage_account.storage_account_resume_rag.name
  storage_account_access_key = azurerm_storage_account.storage_account_resume_rag.primary_access_key
  service_plan_id            = azurerm_service_plan.app_service_plan_resume_rag.id

  site_config {
      application_stack {
        python_version = "3.11"
    }
  }

  tags = var.resume_rag_tags
}

# Outputs
output "resource_group_name" {
  value = azurerm_resource_group.resource_group_resume_rag.name
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