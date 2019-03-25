variable "lambda_function" {
  type = "map"
  default = {
    filename = ""
    function_name = ""
    role = ""
    memory_size = ""
    timeout = ""
    source_code_hash = ""
    memory_size = ""
    layers = ""
  }
}

variable "environment" {
  type        = "map"
  default     = {
  }
}