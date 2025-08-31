terraform {
  backend "azurerm" {
    use_azuread_auth = true
    key              = "state.tfstate"
  }
}

resource "azurerm_resource_group" "warmte_check" {
  name     = "rg-${local.tags.project}-${local.tags.environment}"
  location = "West Europe"

  tags = local.tags
}

resource "random_string" "storage_account_suffix" {
  length = 10

  special = false
  lower   = true
  upper   = false
}

resource "azurerm_storage_account" "warmte_check" {
  name                     = "${local.storage_account_name}${random_string.storage_account_suffix.result}"
  resource_group_name      = azurerm_resource_group.warmte_check.name
  location                 = azurerm_resource_group.warmte_check.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = local.tags

  # In actual production scenarios, you would probably want to prevent the storage_account from being deleted to prevent data loss.
  #   lifecycle {
  #     prevent_destroy = true
  #   }
}

resource "azurerm_storage_container" "data_container" {
  name                  = "warmtecheck"
  storage_account_id    = azurerm_storage_account.warmte_check.id
  container_access_type = "private"
}

resource "azurerm_role_assignment" "function_app_storage" {
  scope                = azurerm_storage_account.warmte_check.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_function_app.warmte_check.identity[0].principal_id

  depends_on = [azurerm_function_app.warmte_check]
}

# In actual production scenarios, you would probably want to prevent the storage_account from being deleted to prevent data loss.
# resource "azurerm_management_lock" "storage_account_lock" {
#   name       = "resource-storage-account"
#   scope      = azurerm_storage_account.warmte_check.id
#   lock_level = "CanNotDelete"
#   notes      = "Locked because the storage account should not be able to be deleted to prevent losing data"

#   depends_on = [azurerm_storage_account.warmte_check]
# }

resource "azurerm_service_plan" "warmte_check" {
  name                = "asp-${local.tags.subscription}-${local.tags.project}-${local.tags.environment}"
  resource_group_name = azurerm_resource_group.warmte_check.name
  location            = azurerm_resource_group.warmte_check.location
  os_type             = "Linux"
  sku_name            = var.service_plan_sku

  tags = local.tags
}

resource "azurerm_linux_function_app" "warmte_check" {
  name                = "example-linux-function-app"
  resource_group_name = azurerm_resource_group.warmte_check.name
  location            = azurerm_resource_group.warmte_check.location

  storage_account_name          = azurerm_storage_account.warmte_check.name
  storage_uses_managed_identity = true
  service_plan_id               = azurerm_service_plan.warmte_check.id

  https_only                    = true
  public_network_access_enabled = true

  identity {
    type = "SystemAssigned"
  }

  site_config {
    app_scale_limit = 1 # Maximum number of instances for demo purposes set to 1
    application_stack {
      python_version = "3.8"
    }
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
    "STORAGE_CONTAINER"        = azurerm_storage_container.data_container.name
  }

  tags = local.tags
}
