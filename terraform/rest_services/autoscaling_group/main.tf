provider "aws" {
  region = data.terraform_remote_state.vpc.outputs.tags.region
}


locals {

  vpc_id         = data.terraform_remote_state.vpc.outputs.vpc_id
  vpc_cidr_block = data.terraform_remote_state.vpc.outputs.vpc_cidr_block

  key_pair = data.terraform_remote_state.vpc.outputs.key_pair

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

  # TODO: incorporate pulling image from AWS ECR
  target_group_arns = data.terraform_remote_state.alb.outputs.target_group_arns
  user_data         = <<EOF
#!/bin/bash
cd /home/ubuntu;

# 1. Env vars
export SOFTWARE_BUILD_VERSION=${var.software_build_version}
export aws_access_key_id=${var.aws_access_key_id};
export aws_secret_access_key=${var.aws_secret_access_key};
export aws_region=${data.terraform_remote_state.vpc.outputs.tags.region}
export ENVIRONMENT=${terraform.workspace};

printenv > .env;

# 2. Export docker-compose file
echo "Export docker-compose file..."
echo "version: '3'
services:

  backend:
    image: 946627858531.dkr.ecr.us-east-2.amazonaws.com/research-kedro-microservice:${var.software_build_version}
    ports:
      - 8000:8000
    env_file: .env
    command: bash -c \"gunicorn
      --bind 0.0.0.0:8000 src.backend.main:app
      --log-config ./local_log_config.ini
      --workers 4
      -k uvicorn.workers.UvicornWorker
      --timeout 1800\"

" > docker-compose.yaml;

# 3. Export aws credentials
echo "[default]" >> .aws_credentials
echo aws_access_key_id = $aws_access_key_id >> .aws_credentials
echo aws_secret_access_key = $aws_secret_access_key >> .aws_credentials
export AWS_CONFIG_FILE=/home/ubuntu/.aws_credentials;

# 4. Authorization
/usr/local/bin/aws --version;
/usr/local/bin/aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 946627858531.dkr.ecr.us-east-2.amazonaws.com


# 4. Start docker-compose
/usr/bin/docker-compose -f docker-compose.yaml up -d
EOF
}


resource "aws_launch_template" "this" {
  name_prefix   = "${local.env}-${local.project_name}-lt"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_types[terraform.workspace]

  monitoring {
    enabled = true
  }

  block_device_mappings {
    device_name = "/dev/sda1"
    ebs {
      volume_size = var.ebs_root_volume_size
    }
  }

  network_interfaces {
    associate_public_ip_address = true
    security_groups = [
      module.asg_sg.security_group_id
    ]
  }

  lifecycle {
    create_before_destroy = true
  }

  user_data              = base64encode(local.user_data)
  update_default_version = true

}


module "asg_sg" {
  version = "= 4.9.0"
  source  = "terraform-aws-modules/security-group/aws"

  name        = "${local.env}-${local.project_name}-asg-sg"
  description = "Security group for application load balancer"
  vpc_id      = local.vpc_id

  ingress_cidr_blocks = [local.vpc_cidr_block]
  ingress_with_cidr_blocks = [
    {
      from_port   = 8000
      to_port     = 8000
      protocol    = "tcp"
      description = "HTTP application ingress traffic allow"
      cidr_blocks = local.vpc_cidr_block
    },
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "Allow ingress ssh traffic"
      cidr_blocks = local.vpc_cidr_block
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


module "asg" {

  source  = "terraform-aws-modules/autoscaling/aws"
  version = "= 6.3.0"

  # Autoscaling group
  name = "${local.env}-${local.project_name}-asg"

  min_size                  = var.min_size[terraform.workspace]
  max_size                  = var.max_size[terraform.workspace]
  desired_capacity          = var.desired_capacity[terraform.workspace]
  wait_for_capacity_timeout = 0
  health_check_type         = "ELB"
  health_check_grace_period = 100
  vpc_zone_identifier       = local.asg_env_subnets_ids
  key_name                  = local.key_pair

  instance_refresh = {
    strategy = "Rolling"
    preferences = {
      min_healthy_percentage = 50
    }
    triggers = ["tag"]
  }

  # Launch template configuration
  create_launch_template = false
  launch_template        = aws_launch_template.this.name
  default_version        = aws_launch_template.this.latest_version

  target_group_arns = local.target_group_arns

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    {
      environment            = local.env
      software_build_version = var.software_build_version
    }
  )

}
