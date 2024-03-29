#####################################
# Athena modules variables.tf
#####################################

variable "tf_bucket" {}
variable "env" {}
variable "region" {}
variable "profile_name" {}

variable "weather_table_name" {}

variable "station_table_name" {}

variable "weather_with_station_id_table_name" {}

variable "weather_athena_database" {
  type = "map"
  default = {
    name = ""
    backet = ""
  }
}
