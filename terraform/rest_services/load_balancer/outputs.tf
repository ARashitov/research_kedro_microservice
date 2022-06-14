output "lb_id" {
  value       = module.alb.lb_id
  description = "The ID and ARN of the load balancer we created."
}

output "target_group_arns" {
  value       = module.alb.target_group_arns
  description = "ARNs of the target groups. Useful for passing to your Auto Scaling group."
}

output "lb_dns_name" {
  value = {
    # stable = "${module.alb.lb_dns_name}:8000"
    latest = "${module.alb.lb_dns_name}:80"
  }
  description = "The DNS name of the load balancer."
}
