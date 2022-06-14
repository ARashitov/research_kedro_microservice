provider "aws" {
  region = data.terraform_remote_state.vpc.outputs.tags.region
}

locals {
  project_name = replace(data.terraform_remote_state.vpc.outputs.tags.project_name, "_", "-")
  name         = "${terraform.workspace}-${local.project_name}"

}

resource "aws_ecr_repository" "ecr" {
  name                 = local.project_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
