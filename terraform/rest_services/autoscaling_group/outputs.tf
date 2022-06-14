output "user_data" {
  sensitive   = true
  value       = local.user_data
  description = "user_data applied to instance"
}

output "software_build_version" {
  value       = var.software_build_version
  description = "Dockerized application build version"
}
