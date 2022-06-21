data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/shared/research_kedro_microservice/vpc.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "alb" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/${terraform.workspace}/research_kedro_microservice/rest_services/alb.tfstate"
    region = "us-east-1"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["946627858531"]

  filter {
    name   = "name"
    values = ["ubuntu-22.04"]
  }

}
