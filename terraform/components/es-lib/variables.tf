#####################################
# S3 modules variables.tf
#####################################

variable "tf_bucket" {}
variable "env" {}
variable "region" {}
variable "profile_name" {}

variable "lambda_layer" {
  type = "map"
  default = {
    filename = ""
    layer_name = ""
  }
}