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
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
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