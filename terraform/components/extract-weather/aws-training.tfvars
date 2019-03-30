env = "aws-training"
region = "ap-northeast-1"
profile_name = "aws-training"

script-location = {
  name = "weather-glue-script20190330"
  acl = "private"
}

"weather-origin-glue-database" = {
  name = "weather_v2"
}

weather-origin-clawler = {
  database_name = "weather_v2"
  name = "weather-origin-clawler"
  role = ""
  table_prefix = "glue"
}

"weather-origin-extract-job" = {
  name = "create_weather_csv"
  role_arn = ""
}