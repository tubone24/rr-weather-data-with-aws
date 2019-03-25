terraform {
  required_version = ">= 0.11.0"

  backend "s3" {
    key    = "es-lib/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

