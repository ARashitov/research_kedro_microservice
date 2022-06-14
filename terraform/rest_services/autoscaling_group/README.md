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
| [terraform_remote_state.alb](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.vpc](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_ami"></a> [ami](#input\_ami) | The AMI from which to launch the instance | `string` | `"ami-08be45d446b4d01f1"` | no |
| <a name="input_any_dynamic_var"></a> [any\_dynamic\_var](#input\_any\_dynamic\_var) | Any dynamic variable used for passing to launch template & further update trigger for instance refresh | `string` | n/a | yes |
| <a name="input_auth_keys_front_and_back"></a> [auth\_keys\_front\_and\_back](#input\_auth\_keys\_front\_and\_back) | Authentication keys passed between frontend and backend | `map(any)` | <pre>{<br>  "prod": "zXhxFv4uPMR6IYt6",<br>  "test": "zXhxFv4uPMR6IYt6",<br>  "ua_test": "zXhxFv4uPMR6IYt6"<br>}</pre> | no |
| <a name="input_aws_access_key_id"></a> [aws\_access\_key\_id](#input\_aws\_access\_key\_id) | aws access key id to use by application | `string` | n/a | yes |
| <a name="input_aws_secret_access_key"></a> [aws\_secret\_access\_key](#input\_aws\_secret\_access\_key) | aws secret access key to use by application | `string` | n/a | yes |
| <a name="input_desired_capacity"></a> [desired\_capacity](#input\_desired\_capacity) | The number of Amazon EC2 instances that should be running in the autoscaling group | `map(any)` | <pre>{<br>  "prod": 1,<br>  "test": 1,<br>  "ua_test": 1<br>}</pre> | no |
| <a name="input_ebs_root_volume_size"></a> [ebs\_root\_volume\_size](#input\_ebs\_root\_volume\_size) | The size of the volume in gigabytes | `number` | `40` | no |
| <a name="input_google_maps_key"></a> [google\_maps\_key](#input\_google\_maps\_key) | google map key to use by application | `string` | n/a | yes |
| <a name="input_instance_types"></a> [instance\_types](#input\_instance\_types) | Default instance types for different application environments | `map(string)` | <pre>{<br>  "prod": "c5a.xlarge",<br>  "test": "c5a.large",<br>  "ua_test": "c5a.large"<br>}</pre> | no |
| <a name="input_key_name"></a> [key\_name](#input\_key\_name) | Key name | `string` | `"aws-us-east-1"` | no |
| <a name="input_latest_stable_release"></a> [latest\_stable\_release](#input\_latest\_stable\_release) | latest docker image to use for deployment | `string` | n/a | yes |
| <a name="input_max_size"></a> [max\_size](#input\_max\_size) | The maximum size of the autoscaling group | `map(any)` | <pre>{<br>  "prod": 1,<br>  "test": 1,<br>  "ua_test": 1<br>}</pre> | no |
| <a name="input_prelatest_stable_release"></a> [prelatest\_stable\_release](#input\_prelatest\_stable\_release) | pre-latest docker image to use for deployment | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_latest_release"></a> [latest\_release](#output\_latest\_release) | Deployed stable latest release version |
| <a name="output_prelatest_release"></a> [prelatest\_release](#output\_prelatest\_release) | Deployed stable pre-latest release version |
| <a name="output_user_data"></a> [user\_data](#output\_user\_data) | user\_data applied to instance |
<!-- END_TF_DOCS -->
