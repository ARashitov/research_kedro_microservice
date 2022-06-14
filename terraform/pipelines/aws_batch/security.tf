resource "aws_iam_role" "ecs_instance_role" {
  name = "${terraform.workspace}__${data.terraform_remote_state.vpc.outputs.tags.project_name}__ecs_instance_role"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
    {
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Principal": {
            "Service": "ec2.amazonaws.com"
        }
    }
    ]
}
EOF

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    {environment = terraform.workspace}
  )
}

resource "aws_iam_role_policy_attachment" "ecs_instance_role" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "ecs_instance_role" {
  name = "${terraform.workspace}__${data.terraform_remote_state.vpc.outputs.tags.project_name}__ecs_instance_role"
  role = aws_iam_role.ecs_instance_role.name

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    {environment = terraform.workspace}
  )
}

resource "aws_iam_role" "aws_batch_service_role" {
  name = "${terraform.workspace}__${data.terraform_remote_state.vpc.outputs.tags.project_name}__aws_batch_service_role"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
    {
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Principal": {
        "Service": "batch.amazonaws.com"
        }
    }
    ]
}
EOF

  tags = merge(
    data.terraform_remote_state.vpc.outputs.tags,
    {environment = terraform.workspace}
  )
}

resource "aws_iam_role_policy_attachment" "aws_batch_service_role" {
  role       = aws_iam_role.aws_batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}
