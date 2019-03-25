#####################################
# S3 modules output.tf
#####################################

output "backet_name" {
  value = "${aws_s3_bucket.s3_bucket.bucket}"
}