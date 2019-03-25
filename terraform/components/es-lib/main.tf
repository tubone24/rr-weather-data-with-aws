module "es-lib" {
  source = "../../modules/lambda/layer"
  lambda_layer = "${var.lambda_layer}"
}