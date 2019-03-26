#####################################
# Athena weather databases
#####################################

locals {
  weather_athena_database = "${merge(
  var.weather_athena_database, map("bucket", data.terraform_remote_state.origin-datas.origin-data-backet-name))}"

  weather_data_bucket =
  "${data.terraform_remote_state.origin-datas.origin-data-backet-name}/${data.terraform_remote_state.origin-datas.weather-datas-prefix}"

  station_data_bucket =
  "${data.terraform_remote_state.origin-datas.origin-data-backet-name}/${data.terraform_remote_state.origin-datas.station-datas-prefix}"
}

data "template_file" "drop_weather_table" {
  template = "${file("sql/weather/drop_table.sql")}"
  vars {
    database_name = "${var.weather_athena_database["name"]}"
    table_name = "${var.weather_table_name}"
  }
}

data "template_file" "create_weather_table" {
  template = "${file("sql/weather/create_table.sql")}"
  vars {
    database_name = "${var.weather_athena_database["name"]}"
    table_name = "${var.weather_table_name}"
    weather_data_bucket = "${local.weather_data_bucket}"
  }
}

data "template_file" "drop_station_table" {
  template = "${file("sql/station/drop_table.sql")}"
  vars {
    database_name = "${var.weather_athena_database["name"]}"
    table_name = "${var.station_table_name}"
  }
}

data "template_file" "create_station_table" {
  template = "${file("sql/station/create_table.sql")}"
  vars {
    database_name = "${var.weather_athena_database["name"]}"
    table_name = "${var.station_table_name}"
    weather_data_bucket = "${local.station_data_bucket}"
  }
}

module "weather_database" {
  source = "../../modules/athena/database"
  athena_database = "${local.weather_athena_database}"
}

resource "aws_athena_named_query" "drop_weather_table" {
  name     = "drop_weather_table"
  database = "${module.weather_database.database_name}"
  query    = "${data.template_file.drop_weather_table.rendered}"
}

resource "aws_athena_named_query" "create_weather_table" {
  name     = "create_weather_table"
  database = "${module.weather_database.database_name}"
  query    = "${data.template_file.create_weather_table.rendered}"
}

resource "aws_athena_named_query" "drop_station_table" {
  name     = "drop_station_table"
  database = "${module.weather_database.database_name}"
  query    = "${data.template_file.drop_station_table.rendered}"
}

resource "aws_athena_named_query" "create_station_table" {
  name     = "create_station_table"
  database = "${module.weather_database.database_name}"
  query    = "${data.template_file.create_station_table.rendered}"
}