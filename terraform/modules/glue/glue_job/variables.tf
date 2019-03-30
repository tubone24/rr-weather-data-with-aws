#####################################
# S3 modules variables.tf
#####################################

variable "glue_crawler" {
  type = "map"
  default = {
    name = ""
    role_arn = ""
    script_location = ""
  }
}