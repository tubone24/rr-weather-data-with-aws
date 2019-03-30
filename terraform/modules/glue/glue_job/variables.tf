#####################################
# glue modules variables.tf
#####################################

variable "glue_job" {
  type = "map"
  default = {
    name = ""
    role_arn = ""
    script_location = ""
  }
}