#####################################
# Athena modules namedquery main.tf
#####################################

resource "aws_athena_named_query" "named_query" {
  name     = "${var.athena_named_query["name"]}"
  database = "${var.athena_named_query["database"]}"
  query    = "${var.athena_named_query["quey"]}"
}