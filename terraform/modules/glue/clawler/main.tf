#####################################
# Glue modules main.tf
#####################################

resource "aws_glue_crawler" "glue_crawler" {
  database_name = "${var.glue_crawler["database_name"]}"
  name          = "${var.glue_crawler["name"]}"
  role          = "${var.glue_crawler["role"]}"
  table_prefix = "${var.glue_crawler["table_prefix"]}"

  s3_target {
    path = "s3://${var.glue_crawler["s3_bucket_path"]}"
  }
}