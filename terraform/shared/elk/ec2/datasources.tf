data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/shared/research_kedro_microservice/vpc.tfstate"
    region = "us-east-1"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["946627858531"]

  filter {
    name   = "name"
    values = ["*ubuntu-22.04-lts-docker*"]
  }

}

data "aws_subnet" "reserved_subnets_id" {
  for_each   = toset(data.terraform_remote_state.vpc.outputs.reserved_subnets_cidr)
  cidr_block = each.key
}

data "terraform_remote_state" "aws_eip" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/shared/research_kedro_microservice/elk/eip.tfstate"
    region = "us-east-1"
  }
}