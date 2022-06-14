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

  # 2. Extraction ASG subnet ids for all environment
  asg_subnets_ids = [
    for cidr_block, subnet_details in data.aws_subnet.asg_subnets_cidr :
    subnet_details["id"]
  ]

  asg_subnets_cidr = [
    for cidr_block, subnet_details in data.aws_subnet.asg_subnets_cidr :
    cidr_block
  ]

  # 3. Extraction ASG subnet id for particular enviornment of TF_WORKSPACE
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

export SOFTWARE_BUILD_VERSION=${var.software_build_version}

# 1. Export nginx configs
echo "
user  nginx;
worker_processes 10;

events {
    worker_connections   1000;
}
http {
    sendfile on;
    underscores_in_headers on;
    proxy_read_timeout 5;
    proxy_connect_timeout 5;
    proxy_send_timeout 5;
    send_timeout 5;

    server {
      listen 8000;

      location / {
        return 200 'Succesfull reach instance!';
      }

    }
}
" > nginx.conf

# 2. Export docker-compose file
echo "Export docker-compose file..."
echo "version: '3'
services:

  nginx:
    image: nginx:1.21.6
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - 8000:8000

" > docker-compose.yaml;

# 2. Start docker-compose
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
