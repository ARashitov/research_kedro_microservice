<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0.8 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | = 4.9.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 4.9.0 |
| <a name="provider_terraform"></a> [terraform](#provider\_terraform) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_asg"></a> [asg](#module\_asg) | terraform-aws-modules/autoscaling/aws | = 6.3.0 |
| <a name="module_asg_sg"></a> [asg\_sg](#module\_asg\_sg) | terraform-aws-modules/security-group/aws | = 4.9.0 |

## Resources

| Name | Type |
|------|------|
| [aws_launch_template.this](https://registry.terraform.io/providers/hashicorp/aws/4.9.0/docs/resources/launch_template) | resource |
| [aws_ami.ubuntu](https://registry.terraform.io/providers/hashicorp/aws/4.9.0/docs/data-sources/ami) | data source |
| [aws_subnet.asg_subnets_cidr](https://registry.terraform.io/providers/hashicorp/aws/4.9.0/docs/data-sources/subnet) | data source |
| [terraform_remote_state.alb](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.vpc](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_desired_capacity"></a> [desired\_capacity](#input\_desired\_capacity) | The number of Amazon EC2 instances that should be running in the autoscaling group | `map(any)` | <pre>{<br>  "prod": 2,<br>  "test": 2,<br>  "ua_test": 2<br>}</pre> | no |
| <a name="input_ebs_root_volume_size"></a> [ebs\_root\_volume\_size](#input\_ebs\_root\_volume\_size) | The size of the volume in gigabytes | `number` | `40` | no |
| <a name="input_instance_types"></a> [instance\_types](#input\_instance\_types) | Default instance types for different application environments | `map(string)` | <pre>{<br>  "prod": "t3a.small",<br>  "test": "t3a.small",<br>  "ua_test": "t3a.small"<br>}</pre> | no |
| <a name="input_max_size"></a> [max\_size](#input\_max\_size) | The maximum size of the autoscaling group | `map(any)` | <pre>{<br>  "prod": 4,<br>  "test": 4,<br>  "ua_test": 4<br>}</pre> | no |
| <a name="input_min_size"></a> [min\_size](#input\_min\_size) | The minimum size of the autoscaling group | `map(any)` | <pre>{<br>  "prod": 1,<br>  "test": 1,<br>  "ua_test": 1<br>}</pre> | no |
| <a name="input_software_build_version"></a> [software\_build\_version](#input\_software\_build\_version) | Dockerized application build version | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_software_build_version"></a> [software\_build\_version](#output\_software\_build\_version) | Dockerized application build version |
| <a name="output_user_data"></a> [user\_data](#output\_user\_data) | user\_data applied to instance |
<!-- END_TF_DOCS -->
