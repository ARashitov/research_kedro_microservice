output "ecr_repository_url" {
  value       = local.ecr_repository_url
  description = "ECR repository url"
}

output "project_name" {
  value       = local.project_name
  description = ""
}

output "env" {
  value       = local.env
  description = ""
}

output "aws_batch_env_subnets_ids" {
  value       = local.aws_batch_env_subnets_ids
  description = ""
}

output "aws_batch_subnets_ids" {
  value       = local.aws_batch_subnets_ids
  description = ""
}

# output "aws_batch_subnets_cidr" {
#   value       = local.aws_batch_subnets_cidr
#   description = ""
# }

output "docker_image_id" {
  value       = local.docker_image_id
  description = "Docker image build"
}

output "ce_instance_type" {
  value       = var.instance_types[terraform.workspace]
  description = "Docker image build"
}

# output "registry_id" {
#   value       = aws_ecr_repository.ecr.registry_id
#   description = "The registry ID where the repository was created."
# }
