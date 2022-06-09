variable "tags" {
  default = {
    project_name = "research-kedro-microservice"
    region       = "us-east-2"
  }
  description = "Tags set to VPC"
  type        = map(string)
}

variable "amt_asg_subnets_per_env" {
  type        = number
  default     = 2
  description = "Amount of subnets for each autoscaling service under project environments"
}

variable "amt_aws_batch_subnets_per_env" {
  type        = number
  default     = 2
  description = "Amount of subnets for each aws batch service under project environments"
}

variable "amt_reserved_subnets_per_env" {
  type        = number
  default     = 1
  description = "Amount of reserved subnets under project environments"
}

variable "environments" {
  type = list(string)
  default = [
    "test",
    "ua_test",
    "prod",
  ]
  description = "Environments used in project"
}

variable "key_pair" {
  type = string
  default = "aws-us-east-2.pem"
  description = "aws instance key used for ssh"
}
