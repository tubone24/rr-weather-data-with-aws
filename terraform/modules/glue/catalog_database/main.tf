#####################################
# Glue modules main.tf
#####################################

resource "aws_glue_catalog_database" "glue_catalog_database" {
  name = "${var.glue_catalog_database.name}"
}