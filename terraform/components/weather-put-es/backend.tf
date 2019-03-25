terraform {
  required_version = ">= 0.11.0"

  backend "s3" {
    key    = "weather-put-es/terraform.tfstate"
    region = "ap-northeast-1"
  }
}