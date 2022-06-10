output "tags" {
  value       = var.tags
  description = "Tags assigned to project"
}

output "vpc_cidr_block" {
  value       = module.vpc.vpc_cidr_block
  description = "VPC CIDR blocks"
}

output "vpc_id" {
  value       = module.vpc.vpc_id
  description = "VPC id"
}

output "default_vpc_cidr_block" {
  value       = module.vpc.default_vpc_cidr_block
  description = "The CIDR block of the Default VPC"
}

output "default_vpc_default_security_group_id" {
  value       = module.vpc.default_vpc_default_security_group_id
  description = "Default security group name"
}

output "default_security_group_id" {
  value       = module.vpc.default_security_group_id
  description = "VPC default security group id"
}

output "amt_asg_subnets_per_env" {
  value       = var.amt_asg_subnets_per_env
  description = "Amount of subnets for each autoscaling service under project environments"
}

output "amt_aws_batch_subnets_per_env" {
  value       = var.amt_aws_batch_subnets_per_env
  description = "Amount of subnets for each aws batch service under project environments"
}

output "amt_reserved_subnets_per_env" {
  value       = var.amt_reserved_subnets_per_env
  description = "Amount of reserved subnets under project environments"
}

output "environments" {
  value       = var.environments
  description = "Environments used in project"
}

output "n_total_subnets" {
  value       = local.n_total_subnets
  description = "Total amount of subnets created under VPC for all environments"
}

output "n_reserved_subnets" {
  value       = local.n_reserved_subnets
  description = "Total amount of reserved subnets created under VPC for all environments"
}

output "n_asg_subnets" {
  value       = local.n_asg_subnets
  description = "Total amount of asg subnets created under VPC for all environments"
}

output "n_aws_batch_subnets" {
  value       = local.n_aws_batch_subnets
  description = "Total amount of aws batch subnets created under VPC for all environments"
}

output "reserved_subnets_cidr" {
  value       = local.reserved_subnets_cidr
  description = "CIDR blocks of reserved subnets"
}

output "asg_subnets_cidr" {
  value       = local.asg_subnets_cidr
  description = "CIDR blocks of asg subnets"
}

output "aws_batch_subnets_cidr" {
  value       = local.aws_batch_subnets_cidr
  description = "CIDR blocks of aws batch subnets"
}

output "cidr_start_octect_reserved" {
  value       = local.start_octect_reserved
  description = "CIDR starting octect value for reserved subnet"
}

output "cidr_end_octect_reserved" {
  value       = local.end_octect_reserved
  description = "CIDR ending octect value for reserved subnet"
}

output "cidr_start_octect_asg" {
  value       = local.start_octect_asg
  description = "CIDR starting octect value for auto-scaling subnet"
}

output "cidr_end_octect_asg" {
  value       = local.end_octect_asg
  description = "CIDR ending octect value for auto-scaling subnet"
}

output "cidr_start_octect_aws_batch" {
  value       = local.start_octect_aws_batch
  description = "CIDR starting octect value for aws batch subnet"
}

output "cidr_end_octect_aws_batch" {
  value       = local.end_octect_aws_batch
  description = "CIDR ending octect value for aws batch subnet"
}

output "key_pair" {
  value       = var.key_pair
  description = "aws instance key used for ssh"
}

