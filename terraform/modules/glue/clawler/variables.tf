#####################################
# S3 modules variables.tf
#####################################

variable "glue_crawler" {
  type = "map"
  default = {
    database_name = ""
    name = ""
    role = ""
    table_prefix = ""
    s3_bucket_path = ""
  }
}