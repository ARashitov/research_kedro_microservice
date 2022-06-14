locals {

  vpc_id         = data.terraform_remote_state.vpc.outputs.vpc_id
  vpc_cidr_block = data.terraform_remote_state.vpc.outputs.vpc_cidr_block

  ecr_repository_url = data.terraform_remote_state.ecr.outputs.repository_url

  environments = data.terraform_remote_state.vpc.outputs.environments
  env_idx      = index(data.terraform_remote_state.vpc.outputs.environments, terraform.workspace)

  project_name = replace(data.terraform_remote_state.vpc.outputs.tags.project_name, "_", "-")
  env          = replace(terraform.workspace, "_", "-")

  # 1. Extraction Batch subnet partioning details
  n_aws_batch_subnets           = data.terraform_remote_state.vpc.outputs.n_aws_batch_subnets
  amt_aws_batch_subnets_per_env = data.terraform_remote_state.vpc.outputs.amt_aws_batch_subnets_per_env
  aws_batch_subnets_ids         = data.terraform_remote_state.vpc.outputs.aws_batch_subnets_ids

  # 2. Extraction ASG subnet id for particular enviornment of TF_WORKSPACE
  subnet_idx_start_env = local.env_idx * local.amt_aws_batch_subnets_per_env
  subnet_idx_end_env   = (local.env_idx + 1) * local.amt_aws_batch_subnets_per_env
  aws_batch_env_subnets_ids = [
    for subnet_idx_end in range(local.subnet_idx_start_env, local.subnet_idx_end_env) :
    local.aws_batch_subnets_ids[subnet_idx_end]
  ]

}


# resource "aws_batch_compute_environment" "aws_batch_ce" {

#   compute_environment_name = "${terraform.workspace}__${data.terraform_remote_state.vpc.outputs.tags.project_name}"

#   # == META CONFIGS ==
#   lifecycle {
#     create_before_destroy = true
#   }


#   compute_resources {
#     # == GENERAL ==
#     type = "EC2"
#     instance_role = aws_iam_instance_profile.ecs_instance_role.arn

#     # == PERFORMANCE ==
#     instance_type = [
#       "c5a.large",
#     ]

#     max_vcpus = var.max_vcpus
#     min_vcpus = var.min_vcpus

#     # == NETWORK & SECURITY ==
#     security_group_ids = [
#       data.terraform_remote_state.vpc.outputs.default_vpc_sg_id,
#     ]

#     # TODO: Setup subnets extraction
#     subnets = data.terraform_remote_state.vpc.outputs.aws_batch_ec2_subnets

#     tags = merge(
#       data.terraform_remote_state.vpc.outputs.tags,
#       {environment = terraform.workspace}
#     )
#   }

#   # == SECURITY & DEPENDENCY ==
#   service_role = aws_iam_role.aws_batch_service_role.arn
#   type         = "MANAGED"
#   depends_on   = [
#     aws_iam_role_policy_attachment.aws_batch_service_role
#   ]

#   tags = merge(
#     data.terraform_remote_state.vpc.outputs.tags,
#     {environment = terraform.workspace}
#   )
# }


# resource "aws_batch_job_definition" "aws_batch_job_def" {

#   name = "${terraform.workspace}__${data.terraform_remote_state.vpc.outputs.tags.project_name}"
#   type = "container"

#   container_properties = <<CONTAINER_PROPERTIES
# {
# TODO: add software build as image to docker
#     "image": "${var.docker_image_id}",
#     "memory": ${var.docker_memory},
#     "vcpus": ${var.docker_vcpus},
#     "volumes": [
#       {
#         "host": {
#           "sourcePath": "/tmp"
#         },
#         "name": "tmp"
#       }
#     ],
#     "environment": [
#         {"name": "aws_access_key_id", "value": "${var.aws_access_key_id}"},
#         {"name": "aws_secret_access_key", "value": "${var.aws_secret_access_key}"}
#     ],
#     "mountPoints": [
#         {
#           "sourceVolume": "tmp",
#           "containerPath": "/tmp",
#           "readOnly": false
#         }
#     ]
# }
# CONTAINER_PROPERTIES

#   tags = merge(
#     data.terraform_remote_state.vpc.outputs.tags,
#     {environment = terraform.workspace}
#   )

# }

# resource "aws_batch_job_queue" "queue" {
# TODO: update names of resources
#   name     = "${terraform.workspace}__${data.terraform_remote_state.vpc.outputs.tags.project_name}"
#   state    = "ENABLED"
#   priority = 1
#   compute_environments = [
#     aws_batch_compute_environment.aws_batch_ce.arn,
#   ]

#   tags = merge(
#     data.terraform_remote_state.vpc.outputs.tags,
#     {environment = terraform.workspace}
#   )

# }
