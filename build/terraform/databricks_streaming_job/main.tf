data "azurerm_key_vault_secret" "storage_account_key" {
  name         = "timeseries-storage-account-key"
  key_vault_id = var.keyvault_id
}

data "azurerm_key_vault_secret" "evhar_inboundqueue_receiver_connection_string" {
  name         = "evhar-inboundqueue-receiver-connection-string"
  key_vault_id = var.keyvault_id
}

module "streaming_job" {
  source                                         = "../job_modules/streaming_job"
  databricks_id                                  = var.databricks_id
  module_name                                    = "StreamingJob"
  storage_account_name                           = var.storage_account_name
  storage_account_key                            = data.azurerm_key_vault_secret.storage_account_key.value
  streaming_container_name                       = var.streaming_container_name
  input_eventhub_listen_connection_string        = data.azurerm_key_vault_secret.evhar_inboundqueue_receiver_connection_string.value
  wheel_file                                     = var.wheel_file
  python_main_file                               = var.python_main_file
}
