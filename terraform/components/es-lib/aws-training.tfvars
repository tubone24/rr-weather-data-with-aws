env = "aws-training"
region = "ap-northeast-1"
profile_name = "aws-training"

lambda_layer = {
  filename = "zip_layer/eslib.zip"
  layer_name = "weather-es-library-v2"
}