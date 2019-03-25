#####################################
# athena modules database variables.tf
#####################################

variable "athena_database" {
  type = "map"
  default = {
    name = ""
    backet = ""
  }
}
