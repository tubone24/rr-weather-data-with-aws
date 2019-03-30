#####################################
# Glue modules main.tf
#####################################

resource "aws_glue_job" "glue_job" {
  name     = "${var.glue_job["name"]}"
  role_arn = "${var.glue_job["role_arn"]}"

  command {
    script_location = "s3://${var.glue_job["script_location"]}/${var.glue_job["name"]}.py"
  }
  default_arguments {
    "--enable-glue-datacatalog" = ""
  }
}