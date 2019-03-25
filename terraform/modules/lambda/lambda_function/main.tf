#####################################
# Lambda
#####################################
resource "aws_lambda_function" "lambda_function" {
  filename         = "${var.lambda_function["filename"]}"
  function_name    = "${var.lambda_function["function_name"]}"
  role             = "${var.lambda_function["role"]}"
  handler          = "lambda_function.lambda_handler"
  timeout          = "${var.lambda_function["timeout"]}"
  runtime          = "python3.6"
  source_code_hash = "${var.lambda_function["source_code_hash"]}"
  memory_size      = "${var.lambda_function["memory_size"]}"
  layers = ["${var.lambda_function[layers]}"]


  environment = ["${slice( list(var.environment), 0, length(var.environment) == 0 ? 0 : 1 )}"]
}