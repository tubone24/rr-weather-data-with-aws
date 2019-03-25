#####################################
# Athena modules database main.tf
#####################################

resource "aws_athena_database" "athena_database" {
  name = "${var.athena_database["name"]}"
  bucket = "${var.athena_database["bucket"]}"
}