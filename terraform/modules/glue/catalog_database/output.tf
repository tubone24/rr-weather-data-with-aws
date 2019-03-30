#####################################
# Glue modules output.tf
#####################################

output "name" {
  value = "${aws_glue_catalog_database.glue_catalog_database.name}"
}