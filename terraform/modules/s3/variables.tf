#####################################
# S3 modules variables.tf
#####################################

variable "s3_bucket" {
  type = "map"
  default = {
    name = ""
    acl = ""
  }
}
