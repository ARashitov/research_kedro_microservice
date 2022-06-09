provider "aws" {
  region = var.tags.region
}

locals {

  n_envs = length(var.environments)

  # Subnets counting
  n_reserved_subnets  = local.n_envs * var.amt_reserved_subnets_per_env
  n_asg_subnets       = local.n_envs * var.amt_asg_subnets_per_env
  n_aws_batch_subnets = local.n_envs * var.amt_aws_batch_subnets_per_env
  n_total_subnets     = local.n_reserved_subnets + local.n_asg_subnets + local.n_aws_batch_subnets

  # NOTE: 3rd octet must be used for only one thing at a time
  # 1st: reserved subnets for all project environments
  # 2nd: auto scaling group subnets for all project environments
  # 3rd: aws batch subnets for all project environments
  start_octect_reserved = 0
  end_octect_reserved   = local.n_reserved_subnets

  start_octect_asg = local.n_reserved_subnets
  end_octect_asg   = local.start_octect_asg + local.n_asg_subnets

  start_octect_aws_batch = local.end_octect_asg
  end_octect_aws_batch   = local.start_octect_aws_batch + local.n_aws_batch_subnets

  # Dynamic computation of subnet octets for services
  reserved_subnets_cidr = [
    for subnet_id in range(local.start_octect_reserved, local.end_octect_reserved) :
    "10.99.${subnet_id}.0/24"
  ]

  asg_subnets_cidr = [
    for subnet_id in range(local.start_octect_asg, local.end_octect_asg) :
    "10.99.${subnet_id}.0/24"
  ]

  aws_batch_subnets_cidr = [
    for subnet_id in range(local.start_octect_aws_batch, local.end_octect_aws_batch) :
    "10.99.${subnet_id}.0/24"
  ]

}


module "vpc" {

  # TODO:
  # 1. Reallocate ASG to private subnets
  # 2. Reallocate AWS batch to private subnets
  # 3. Enable NAT
  source  = "terraform-aws-modules/vpc/aws"
  version = "= 3.14.0"

  name = var.tags.project_name
  cidr = "10.99.0.0/18"

  azs = ["${var.tags.region}a", "${var.tags.region}b", "${var.tags.region}c"]

  public_subnets = concat(
    local.reserved_subnets_cidr,
    local.asg_subnets_cidr,
    local.aws_batch_subnets_cidr,
  )

  private_subnets = []

  enable_dns_hostnames = true
  enable_dns_support   = true

  manage_default_security_group = true

  default_security_group_egress = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = "0.0.0.0/0"
      description = "Allow entire egress traffic"
    }
  ]
  default_security_group_ingress = [
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = "0.0.0.0/0"
      description = "Allow ssh ingress traffic"
    },
  ]

  tags = merge(
    var.tags,
    {
      environment = terraform.workspace,
    }
  )
}
