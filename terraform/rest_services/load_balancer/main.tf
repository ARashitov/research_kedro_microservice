provider "aws" {
  region = data.terraform_remote_state.vpc.outputs.tags.region
}

locals {

  vpc_id = data.terraform_remote_state.vpc.outputs.vpc_id

  environments = data.terraform_remote_state.vpc.outputs.environments
  env_idx      = index(data.terraform_remote_state.vpc.outputs.environments, terraform.workspace)

  project_name = replace(data.terraform_remote_state.vpc.outputs.tags.project_name, "_", "-")
  env          = replace(terraform.workspace, "_", "-")

  # 1. Extraction ASG subnet portioning details
  n_asg_subnets           = data.terraform_remote_state.vpc.outputs.n_asg_subnets
  amt_asg_subnets_per_env = data.terraform_remote_state.vpc.outputs.amt_asg_subnets_per_env
  asg_subnets_ids         = data.terraform_remote_state.vpc.outputs.asg_subnets_ids

  # 2. Extraction ASG subnet id for particular enviornment of TF_WORKSPACE
  subnet_idx_start_env = local.env_idx * local.amt_asg_subnets_per_env
  subnet_idx_end_env   = (local.env_idx + 1) * local.amt_asg_subnets_per_env
  asg_env_subnets_ids = [
    for subnet_idx_end in range(local.subnet_idx_start_env, local.subnet_idx_end_env) :
    local.asg_subnets_ids[subnet_idx_end]
  ]

}


module "alb_sg" {
  version = "= 4.9.0"
  source  = "terraform-aws-modules/security-group/aws"

  name        = "${local.env}-kedro-microservice"
  description = "Security group for application load balancer"
  vpc_id      = local.vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_with_cidr_blocks = [
    {
      from_port   = var.http_listener_port
      to_port     = var.http_listener_port
      protocol    = "tcp"
      description = "Rest API endpoint port"
      cidr_blocks = "0.0.0.0/0"
    },
  ]

  egress_cidr_blocks = ["0.0.0.0/0"]
  egress_with_cidr_blocks = [
    {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = "0.0.0.0/0"
      description = "Allow entire egress traffic"
    }
  ]
}


module "alb" {
  # TODO: configure route53 as DNS for application
  source  = "terraform-aws-modules/alb/aws"
  version = "= 6.4.0"

  name = "${local.env}-kedro-microservice"

  vpc_id          = local.vpc_id
  subnets         = local.asg_env_subnets_ids
  security_groups = [module.alb_sg.security_group_id]

  idle_timeout = 1800

  http_tcp_listeners = [
    {
      port               = var.http_listener_port
      protocol           = "HTTP"
      target_group_index = 0
    },
  ]

  target_groups = [
    {
      name             = "${local.env}-kedro-microservice"
      backend_protocol = "HTTP"
      backend_port     = var.http_backend_port
      target_type      = "instance"
      health_check = {
        enabled  = true
        interval = 10
        path     = "/"
        protocol = "HTTP"
        matcher  = "200-399"
      }
    },
  ]

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    { environment = local.env }
  )
}
