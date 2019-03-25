#####################################
# S3 modules main.tf
#####################################

resource "aws_s3_bucket" "s3_bucket" {
  bucket = "${var.s3_bucket["name"]}"
  acl    = "${var.s3_bucket["acl"]}"
}