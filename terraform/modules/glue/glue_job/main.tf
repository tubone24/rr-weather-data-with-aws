#####################################
# Glue modules main.tf
#####################################

resource "aws_glue_job" "glue_job" {
  name     = "${var.glue_crawler.name}"
  role_arn = "${var.glue_crawler.role_arn}"

  command {
    script_location = "s3://${var.glue_crawler.script_location}/${var.glue_crawler.name}.py"
  }
  default_arguments {
    "--enable-glue-datacatalog" = ""
  }
}

