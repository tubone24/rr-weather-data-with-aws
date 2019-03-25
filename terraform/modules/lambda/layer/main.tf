#####################################
# Lambda layer
#####################################
resource "aws_lambda_layer_version" "lambda_layer" {
  filename = "${var.lambda_layer["filename"]}"
  layer_name = "${var.lambda_layer["layer_name"]}"

  compatible_runtimes = ["python3.6"]
}