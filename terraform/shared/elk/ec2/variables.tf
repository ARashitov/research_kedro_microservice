variable "instance_type" {
  type        = string
  description = "Default instance type for proxy instance"
  # default     = "c5a.large"
  default = "t2.micro"
}
