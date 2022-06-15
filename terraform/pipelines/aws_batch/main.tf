provider "aws" {
  region = data.terraform_remote_state.vpc.outputs.tags.region
}

locals {
  region         = data.terraform_remote_state.vpc.outputs.tags.region
  vpc_id         = data.terraform_remote_state.vpc.outputs.vpc_id
  vpc_cidr_block = data.terraform_remote_state.vpc.outputs.vpc_cidr_block

  default_security_group_id = data.terraform_remote_state.vpc.outputs.default_security_group_id
  key_pair                  = data.terraform_remote_state.vpc.outputs.key_pair

  ecr_repository_url = data.terraform_remote_state.ecr.outputs.repository_url

  environments = data.terraform_remote_state.vpc.outputs.environments
  env_idx      = index(data.terraform_remote_state.vpc.outputs.environments, terraform.workspace)

  project_name       = replace(data.terraform_remote_state.vpc.outputs.tags.project_name, "_", "-")
  env                = replace(terraform.workspace, "_", "-")
  short_project_name = "kedro-microservice"

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

  vpc_tags        = data.terraform_remote_state.vpc.outputs.tags
  docker_image_id = "${local.ecr_repository_url}:${var.software_build_version}"

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    { environment = local.env }
  )
}


resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/batch/${local.env}/${local.project_name}"
  retention_in_days = var.logs_retention_in_days
  tags              = local.tags
}


module "batch" {

  source  = "terraform-aws-modules/batch/aws"
  version = ">= 1.1.1, < 2.0.0"

  instance_iam_role_name        = "${local.env}-${local.short_project_name}-ecs-instance"
  instance_iam_role_path        = "/batch/"
  instance_iam_role_description = "IAM instance role/profile for AWS Batch ECS instance(s)"
  instance_iam_role_additional_policies = [
    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  ]
  instance_iam_role_tags = {
    ModuleCreatedRole = "Yes"
  }

  service_iam_role_name        = "${local.env}-${local.short_project_name}-batch"
  service_iam_role_path        = "/batch/"
  service_iam_role_description = "IAM service role for AWS Batch"
  service_iam_role_tags = {
    ModuleCreatedRole = "Yes"
  }

  create_spot_fleet_iam_role      = true
  spot_fleet_iam_role_name        = "${local.env}-${local.short_project_name}-spot"
  spot_fleet_iam_role_path        = "/batch/"
  spot_fleet_iam_role_description = "IAM spot fleet role for AWS Batch"
  spot_fleet_iam_role_tags = {
    ModuleCreatedRole = "Yes"
  }

  compute_environments = {
    # a_ec2 = {
    #   name_prefix = "ec2"

    #   compute_resources = {
    #     type           = "EC2"
    #     min_vcpus      = 4
    #     max_vcpus      = 16
    #     desired_vcpus  = 4
    #     instance_types = var.instance_types[terraform.workspace]

    #     security_group_ids = [local.default_security_group_id]
    #     subnets            = local.aws_batch_env_subnets_ids

    #     # Note - any tag changes here will force compute environment replacement
    #     # which can lead to job queue conflicts. Only specify tags that will be static
    #     # for the lifetime of the compute environment
    #     tags = {
    #       # This will set the name on the Ec2 instances launched by this compute environment
    #       Name = local.name
    #       Type = "Ec2"
    #     }
    #   }
    # }

    b_ec2_spot = {
      name_prefix = "ec2_spot"

      compute_resources = {
        type                = "SPOT"
        allocation_strategy = "SPOT_CAPACITY_OPTIMIZED"
        bid_percentage      = var.max_on_demand_price_percentage

        min_vcpus      = var.min_vcpus[terraform.workspace]
        max_vcpus      = var.max_vcpus[terraform.workspace]
        desired_vcpus  = var.desired_vcpus[terraform.workspace]
        instance_types = var.instance_types[terraform.workspace]

        security_group_ids = [local.default_security_group_id]
        subnets            = local.aws_batch_env_subnets_ids

        # Note - any tag changes here will force compute environment replacement
        # which can lead to job queue conflicts. Only specify tags that will be static
        # for the lifetime of the compute environment
        tags = merge(
          local.tags,
          {
            Name = "${local.env}-${local.project_name}-spot"
            Type = "EC2Spot"
          }
        )

      }
    }

  }

  # Job queus and scheduling policies
  job_queues = {

    high_priority = {
      name     = "${local.env}-${local.project_name}-spot"
      state    = "ENABLED"
      priority = 99

      fair_share_policy = {
        compute_reservation = 1
        share_decay_seconds = 3600

        share_distribution = [{
          share_identifier = "A1*"
          weight_factor    = 0.2
          }, {
          share_identifier = "A2"
          weight_factor    = 0.2
        }]
      }

      tags = local.tags
    }
  }

  job_definitions = {
    default_job_definition = {
      name           = "${local.env}-${local.project_name}-job-definition"
      propagate_tags = true

      container_properties = jsonencode({
        command = ["ls", "-la"]
        image   = local.docker_image_id
        resourceRequirements = [
          { type = "VCPU", value = var.container_vcpu[terraform.workspace] },
          { type = "MEMORY", value = var.container_memory[terraform.workspace] }
        ]
        logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group         = aws_cloudwatch_log_group.this.id
            awslogs-region        = local.region
            awslogs-stream-prefix = "${local.env}-${local.project_name}"
          }
        }
      })

      attempt_duration_seconds = 60
      retry_strategy = {
        attempts = 3
        evaluate_on_exit = {
          retry_error = {
            action       = "RETRY"
            on_exit_code = 1
          }
          exit_success = {
            action       = "EXIT"
            on_exit_code = 0
          }
        }
      }

      tags = local.tags
    }
  }

}
