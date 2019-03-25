#####################################
# athena modules named_query variables.tf
#####################################

variable "athena_named_query" {
  type = "map"
  default = {
    name = ""
    database = ""
    query = ""
  }
}
