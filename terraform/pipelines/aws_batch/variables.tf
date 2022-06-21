variable "logs_retention_in_days" {
  type        = number
  default     = 3
  description = "How long logs must be stored in system"
}

variable "max_on_demand_price_percentage" {
  type        = number
  default     = 70
  description = "Maximum % on-demand price"
}

variable "desired_vcpus" {
  type = map(number)
  default = {
    test    = 2
    ua_test = 2
    prod    = 2
  }
  description = "Desired VCPus to utilize"
}

variable "max_vcpus" {
  type = map(number)
  default = {
    test    = 16
    ua_test = 16
    prod    = 16
  }
  description = "Maximum VCPus to utilize"
}

variable "min_vcpus" {
  type = map(number)
  default = {
    test    = 2
    ua_test = 2
    prod    = 2
  }
  description = "Minimum VCPus to utilize"
}

variable "instance_types" {
  type        = map(list(string))
  description = "Default instance types for different application environments"
  default = {
    test    = ["c5a.large", "c5a.xlarge"]
    ua_test = ["c5a.large", "c5a.xlarge"]
    prod    = ["c5a.large", "c5a.xlarge"]
  }
}

variable "container_vcpu" {
  type        = map(string)
  description = "Amount of VCU to use by docker container"
  default = {
    test    = "2"
    ua_test = "2"
    prod    = "2"
  }
}

variable "container_memory" {
  type        = map(string)
  description = "Amount of VCU to use by docker container"
  default = {
    test    = "3500"
    ua_test = "3500"
    prod    = "3500"
  }
}

variable "software_build_version" {
  type        = string
  default     = "2022-06-21--12-42-03"
  description = "Software build version"
}

variable "aws_access_key_id" {
  type        = string
  description = "aws access key id used for export as env variable to batch job definition"
}

variable "aws_secret_access_key" {
  type        = string
  description = "aws secret access key used for export as env variable to batch job definition"
}
