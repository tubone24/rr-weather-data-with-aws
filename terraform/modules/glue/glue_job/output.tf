#####################################
# Glue modules output.tf
#####################################

output "database_name" {
  value = "${aws_glue_crawler.glue_crawler.database_name}"
}

output "name" {
  value = "${aws_glue_crawler.glue_crawler.name}"
}

output "table_prefix" {
  value = "${aws_glue_crawler.glue_crawler.table_prefix}"
}