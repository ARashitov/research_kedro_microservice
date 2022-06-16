data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/shared/research_kedro_microservice/vpc.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "ecr" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/shared/research_kedro_microservice/ecr.tfstate"
    region = "us-east-1"
  }
}
