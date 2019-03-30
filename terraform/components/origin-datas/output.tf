output "origin-data-backet-name" {
  value = "${module.origin-datas.backet_name}"
}

output "weather-datas-prefix" {
  value = "${local.weather-datas-prefix}"
}

output "station-datas-prefix" {
  value = "${local.station-datas-prefix}"
}

output "weather-with-station-id-prefix" {
  value = "${local.weather-with-station-id-prefix}"
}