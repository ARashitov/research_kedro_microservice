resource "aws_batch_compute_environment" "aws_batch_ce" {

  compute_environment_name = "${terraform.workspace}__${data.terraform_remote_state.vpc.outputs.tags.project_name}"

  # == META CONFIGS ==
  lifecycle {
    create_before_destroy = true
  }


  compute_resources {
    # == GENERAL ==
    type = "EC2"
    instance_role = aws_iam_instance_profile.ecs_instance_role.arn

    # == PERFORMANCE ==
    instance_type = [
      "c5a.large",
    ]

    max_vcpus = var.max_vcpus
    min_vcpus = var.min_vcpus

    # == NETWORK & SECURITY ==
    security_group_ids = [
      data.terraform_remote_state.vpc.outputs.default_vpc_sg_id,
    ]

    subnets = data.terraform_remote_state.vpc.outputs.aws_batch_ec2_subnets

    tags = merge(
      data.terraform_remote_state.vpc.outputs.tags,
      {environment = terraform.workspace}
    )
  }

  # == SECURITY & DEPENDENCY ==
  service_role = aws_iam_role.aws_batch_service_role.arn
  type         = "MANAGED"
  depends_on   = [
    aws_iam_role_policy_attachment.aws_batch_service_role
  ]

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    {environment = terraform.workspace}
  )
}


resource "aws_batch_job_definition" "aws_batch_job_def" {

  name = "${terraform.workspace}__${data.terraform_remote_state.vpc.outputs.tags.project_name}"
  type = "container"

  container_properties = <<CONTAINER_PROPERTIES
{
    "image": "${var.docker_image_id}",
    "memory": ${var.docker_memory},
    "vcpus": ${var.docker_vcpus},
    "volumes": [
      {
        "host": {
          "sourcePath": "/tmp"
        },
        "name": "tmp"
      }
    ],
    "environment": [
        {"name": "aws_access_key_id", "value": "${var.aws_access_key_id}"},
        {"name": "aws_secret_access_key", "value": "${var.aws_secret_access_key}"}
    ],
    "mountPoints": [
        {
          "sourceVolume": "tmp",
          "containerPath": "/tmp",
          "readOnly": false
        }
    ]
}
CONTAINER_PROPERTIES

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    {environment = terraform.workspace}
  )

}

resource "aws_batch_job_queue" "queue" {
  name     = "${terraform.workspace}__${data.terraform_remote_state.vpc.outputs.tags.project_name}"
  state    = "ENABLED"
  priority = 1
  compute_environments = [
    aws_batch_compute_environment.aws_batch_ce.arn,
  ]

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    {environment = terraform.workspace}
  )

}
