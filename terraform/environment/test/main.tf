provider "azurerm" {
  tenant_id       = "${var.tenant_id}"
  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  features {}
}
terraform {
  backend "azurerm" {
    storage_account_name = "storage5132022"
    container_name       = "container5132022"
    key                  = "terraform.tfstate"
    access_key           = "dc858lRyDghyVlyPL57+Www9iSfz0aNh0G8DD48vV+ddZzFdRpTfzxzJLxKQUB8/f/n/Zth+IAHlp57NFST3cA=="
  }
}

module "network" {
  source               = "../../modules/network"
  address_space        = "${var.address_space}"
  location             = "${var.location}"
  virtual_network_name = "${var.virtual_network_name}"
  application_type     = "${var.application_type}"
  resource_type        = "NET"
  resource_group       = "${var.resource_group}"
  address_prefix_test  = "${var.address_prefix_test}"
}

module "nsg-test" {
  source           = "../../modules/networksecuritygroup"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "NSG"
  resource_group   = "${var.resource_group}"
  subnet_id        = "${module.network.subnet_id_test}"
  address_prefix_test = "${var.address_prefix_test}"
}
module "appservice" {
  source           = "../../modules/appservice"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "AppService"
  resource_group   = "${var.resource_group}"
}
module "publicip" {
  source           = "../../modules/publicip"
  location         = "${var.location}"
  application_type = "${var.application_type}"
  resource_type    = "publicip"
  resource_group   = "${var.resource_group}"
}

module "vm" {
  source               = "../../modules/vm"
  location             = "${var.location}"
  application_type     = "${var.application_type}"
  resource_type        = "VM"
  resource_group       = "${var.resource_group}"
  admin_username       = "${var.admin_username}"
  public_ip_address_id = "${module.publicip.public_ip_address_id}"
  subnet_id            = "${module.network.subnet_id_test}"
}