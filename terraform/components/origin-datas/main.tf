#####################################
# Origin datas S3 backet
#####################################

locals {
  weather-datas-prefix = "weather-datas/"
  station-datas-prefix = "station-datas/"
  weather-with-station-id-prefix = "weather-with-station-id/"
}

module "origin-datas" {
  source = "../../modules/s3"
  s3_bucket = "${var.origin-datas}"
}

resource "aws_s3_bucket_object" "prefix-weather-datas" {
  bucket = "${module.origin-datas.backet_name}"
  acl    = "private"
  key    = "${local.weather-datas-prefix}"
  source = "/dev/null"
}

resource "aws_s3_bucket_object" "prefix-station-datas" {
  bucket = "${module.origin-datas.backet_name}"
  acl    = "private"
  key    = "${local.station-datas-prefix}"
  source = "/dev/null"
}