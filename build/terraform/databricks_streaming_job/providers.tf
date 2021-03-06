#Set the terraform required version
terraform {
  required_version = ">= 0.12.6"

  required_providers {
    databricks = {
      source = "databrickslabs/databricks"
      version = "0.2.5"
    }
  }
}

provider "databricks" {
  azure_workspace_resource_id = var.databricks_id
}

provider "azurerm" {
  features {}
}