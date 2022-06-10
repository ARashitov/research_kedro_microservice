# output "lb_id" {
#   value       = module.alb.lb_id
#   description = "The ID and ARN of the load balancer we created."
# }

# output "target_group_arns" {
#   value       = module.alb.target_group_arns
#   description = "ARNs of the target groups. Useful for passing to your Auto Scaling group."
# }

# output "lb_dns_name" {
#   value = {
#     # stable = "${module.alb.lb_dns_name}:8000"
#     latest = "${module.alb.lb_dns_name}:8001"
#   }
#   description = "The DNS name of the load balancer."
# }

output "env" {
  value = local.env
  description = ""
}

output "env_idx" {
  value = local.env_idx
  description = ""
}

output "asg_subnets_ids" {
  value = local.asg_subnets_ids
  description = ""
}

output "asg_subnets_cidr" {
  value = local.asg_subnets_cidr
  description = ""
}

output "subnet_idx_start_env" {
  value = local.subnet_idx_start_env
  description = ""
}

output "subnet_idx_end_env" {
  value = local.subnet_idx_end_env
  description = ""
}

output "asg_env_subnets_ids" {
  value = local.asg_env_subnets_ids
  description = ""
}