variable "instance_types" {
  type        = map(string)
  description = "Default instance types for different application environments"
  default = {
    test    = "t3a.small"
    ua_test = "t3a.small"
    prod    = "t3a.small"
  }
}

variable "min_size" {
  type        = map(any)
  description = "The minimum size of the autoscaling group"
  default = {
    test    = 1
    ua_test = 1
    prod    = 1
  }
}

variable "max_size" {
  type        = map(any)
  description = "The maximum size of the autoscaling group"
  default = {
    test    = 4
    ua_test = 4
    prod    = 4
  }
}

variable "desired_capacity" {
  type        = map(any)
  description = "The number of Amazon EC2 instances that should be running in the autoscaling group"
  default = {
    test    = 2
    ua_test = 2
    prod    = 2
  }
}

variable "ebs_root_volume_size" {
  type        = number
  description = "The size of the volume in gigabytes"
  default     = 40
}

variable "software_build_version" {
  type        = string
  description = "Dockerized application build version"
  default = "2022-06-21--12-42-03"
}

variable "aws_access_key_id" {
  description = "aws access key id to use by application"
  type        = string
}

variable "aws_secret_access_key" {
  description = "aws secret access key to use by application"
  type        = string
}

# variable "auth_keys_front_and_back" {
#   type        = map(any)
#   description = "Authentication keys passed between frontend and backend"
#   default = {
#     test    = "zXhxFv4uPMR6IYt6"
#     ua_test = "zXhxFv4uPMR6IYt6"
#     prod    = "zXhxFv4uPMR6IYt6"
#   }
# }

# variable "aws_access_key_id" {
#   description = "aws access key id to use by application"
#   type        = string
# }

# variable "aws_secret_access_key" {
#   description = "aws secret access key to use by application"
#   type        = string
# }
