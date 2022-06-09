provider "aws" {
  region = data.terraform_remote_state.vpc.outputs.tags.region
}

resource "aws_eip" "lb" {
  vpc = true
}