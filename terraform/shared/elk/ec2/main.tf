provider "aws" {
  region = data.terraform_remote_state.vpc.outputs.tags.region
}


locals {
  name                      = "elk-${terraform.workspace}-${local.project_name}"
  vpc_id                    = data.terraform_remote_state.vpc.outputs.vpc_id
  vpc_cidr_block            = data.terraform_remote_state.vpc.outputs.vpc_cidr_block
  default_security_group_id = data.terraform_remote_state.vpc.outputs.default_security_group_id
  reserved_subnet_ids = [
    for cidr_block, subnet_details in data.aws_subnet.reserved_subnets_id :
    subnet_details["id"]
  ]
  project_name              = replace(data.terraform_remote_state.vpc.outputs.tags.project_name, "_", "-")
  tags                      = data.terraform_remote_state.vpc.outputs.tags
}


module "elk_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.0"

  name        = local.name
  description = "Security group for example usage with EC2 instance"
  vpc_id      = local.vpc_id

  ingress_cidr_blocks = [local.vpc_cidr_block]
  ingress_with_cidr_blocks = [
    {
      from_port   = 5959
      to_port     = 5959
      protocol    = "tcp"
      description = "TCP logstash input"
      cidr_blocks = "0.0.0.0/0"
      # cidr_blocks = local.vpc_cidr_block
    },
    {
      from_port   = 5601
      to_port     = 5601
      protocol    = "tcp"
      description = "Kibana"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      description = "ssh"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port   = 9200
      to_port     = 9200
      protocol    = "tcp"
      description = "TCP logstash input"
      cidr_blocks = "0.0.0.0/0"
      # cidr_blocks = local.vpc_cidr_block
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

  tags = local.tags
}


resource "aws_network_interface" "elk" {
  subnet_id = local.reserved_subnet_ids[0]
  security_groups = [
    local.default_security_group_id,
    module.elk_sg.security_group_id,
  ]
}


resource "aws_eip_association" "elk_eip" {
  allocation_id = data.terraform_remote_state.aws_eip.outputs.id
  network_interface_id = aws_network_interface.elk.id
}


module "ec2" {
  # TODO: establish elk startup over user data
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "= 3.5.0"

  name = local.name

  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = data.terraform_remote_state.vpc.outputs.key_pair
  monitoring    = true

  network_interface = [
    {
      device_index          = 0
      network_interface_id  = aws_network_interface.elk.id
    }
  ]

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    { environment = terraform.workspace }
  )

}
