terraform {
  backend "azurerm" {
    resource_group_name   = "@resource_group_name"
    storage_account_name  = "@storage_account_name"
    container_name        = "tfstate"
    key                   = "terraform_it_infra.tfstate"
  }
}