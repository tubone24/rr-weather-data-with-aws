locals {
  weather-origin-bucket = "${data.terraform_remote_state.origin-datas.origin-data-backet-name}"
  weather-datas-prefix = "${data.terraform_remote_state.origin-datas.weather-datas-prefix}"
  bucket-weather = "${local.weather-origin-bucket}/${local.weather-datas-prefix}"
  bucket-weather-with-station-id = "${aws_s3_bucket_object.prefix-weather-with-station-id.bucket}/${local.weather-with-station-id-prefix}"
  weather-origin-clawler = "${merge(var.weather-origin-clawler, map("s3_bucket_path", "${local.bucket-weather}"))}"
  weather-with-station-id-prefix = "${data.terraform_remote_state.origin-datas.weather-with-station-id-prefix}"
  script_location = "${module.script-location.backet_name}"
  weather-origin-extract-job = "${merge(var.weather-origin-extract-job, map("script_location", local.script_location))}"
}

#####################################
# glue job scripts datas S3 backet
#####################################

module "script-location" {
  source = "../../modules/s3"
  s3_bucket = "${var.script-location}"
}

#####################################
# Upload glue job script to s3
#####################################

data "template_file" "create_weather_csv_tpl" {
  template = "${file("scripts/create_weather_csv.py.tpl")}"
  vars {
    weather-database = "${var.weather-origin-glue-database["name"]}"
    weather-table-name = "${module.weather-origin-clawler.table_prefix}weather_datas"
    weather-origin-bucket = "${local.weather-origin-bucket}"
    weather-datas-prefix = "${local.weather-datas-prefix}"
    weather-with-station-id-prefix = "${local.weather-with-station-id-prefix}"
  }
}

resource "local_file" "create_weather_csv" {
  content     = "${data.template_file.create_weather_csv_tpl.rendered}"
  filename = "scripts/create_weather_csv.py"
}

resource "aws_s3_bucket_object" "upload-glue-job-script" {
  bucket = "${module.script-location.backet_name}"
  acl    = "private"
  key    = "create_weather_csv.py"
  source = "scripts/create_weather_csv.py"
  etag = "${md5("scripts/create_weather_csv.py")}"
}

#####################################
# with station_id datas S3 backet
#####################################

resource "aws_s3_bucket_object" "prefix-weather-with-station-id" {
  bucket = "${data.terraform_remote_state.origin-datas.origin-data-backet-name}"
  acl    = "private"
  key    = "${local.weather-with-station-id-prefix}"
  source = "/dev/null"
}

#####################################
# Glue catalog database
#####################################

#module "weather-origin-glue-database" {
#  source = "../../modules/glue/catalog_database"
#  glue_catalog_database = "${var.weather-origin-glue-database}"
#}

#####################################
# Glue Clawler
#####################################

module "weather-origin-clawler" {
  source = "../../modules/glue/clawler"
  glue_crawler = "${local.weather-origin-clawler}"
}

#####################################
# Glue Job
#####################################

module "weather-origin-extract-job" {
  source = "../../modules/glue/glue_job"
  glue_job = "${local.weather-origin-extract-job}"
}