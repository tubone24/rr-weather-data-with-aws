#####################################
# S3 modules variables.tf
#####################################

variable "tf_bucket" {}
variable "env" {}
variable "region" {}
variable "profile_name" {}

variable "origin-datas" {
  type = "map"
  default = {
    name = ""
    acl = ""
  }
}
