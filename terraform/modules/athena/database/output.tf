#####################################
# Athena modules database output.tf
#####################################

output "database_name" {
  value = "${aws_athena_database.athena_database.name}"
}