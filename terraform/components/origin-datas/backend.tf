terraform {
  required_version = ">= 0.11.0"

  backend "s3" {
    key    = "origin-datas/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

