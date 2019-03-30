#####################################
# S3 modules variables.tf
#####################################

variable "glue_catalog_database" {
  type = "map"
  default = {
    name = ""
  }
}