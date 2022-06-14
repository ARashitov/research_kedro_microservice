data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/shared/research_kedro_microservice/vpc.tfstate"
    region = "us-east-1"
  }
}

data "aws_subnet" "asg_subnets_cidr" {
  for_each   = toset(data.terraform_remote_state.vpc.outputs.asg_subnets_cidr)
  cidr_block = each.key
}
