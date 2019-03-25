terraform {
  required_version = ">= 0.11.0"

  backend "s3" {
    key    = "weather-tables/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

data "terraform_remote_state" "origin-datas" {
  backend = "s3"
  config {
    bucket = "${var.tf_bucket}"
    key = "env:/${var.env}/origin-datas/terraform.tfstate"
    region = "ap-northeast-1"
    profile = "${var.profile_name}"
  }
}
