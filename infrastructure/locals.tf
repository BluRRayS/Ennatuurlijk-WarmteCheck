locals {
  tags = {
    environment  = var.environment
    costcenter   = var.costcenter
    customer     = var.customer
    project      = var.project
    subscription = var.subscription
  }
  storage_account_name = "stwarmtecheckprd"
}
