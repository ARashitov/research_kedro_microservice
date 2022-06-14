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

# output "repository_url" {
#   value       = aws_ecr_repository.ecr.repository_url
#   description = "The URL of the repository (in the form `aws_account_id.dkr.ecr.region.amazonaws.com/repositoryName`)."
# }

# output "registry_id" {
#   value       = aws_ecr_repository.ecr.registry_id
#   description = "The registry ID where the repository was created."
# }
