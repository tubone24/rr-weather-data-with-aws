#####################################
# Glue modules output.tf
#####################################

output "glue_job_name" {
  value = "${aws_glue_job.glue_job.name}"
}

