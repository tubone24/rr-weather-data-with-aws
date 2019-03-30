#####################################
# S3 modules variables.tf
#####################################

variable "tf_bucket" {}
variable "env" {}
variable "region" {}
variable "profile_name" {}

variable "script-location" {
  type = "map"
  default = {
    name = ""
    acl = ""
  }
}

variable "weather-origin-glue-database" {
  type = "map"
  default = {
    name = ""
  }
}

variable "weather-origin-clawler" {
  type = "map"
  default = {
    database_name = ""
    name = ""
    role = ""
    table_prefix = ""
  }
}

variable "weather-origin-extract-job" {
  type = "map"
  default = {
    name = ""
    role_arn = ""
  }
}