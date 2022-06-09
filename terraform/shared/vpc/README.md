<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0.8, < 2.0.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | = 4.9.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_vpc"></a> [vpc](#module\_vpc) | terraform-aws-modules/vpc/aws | = 3.14.0 |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_amt_asg_subnets_per_env"></a> [amt\_asg\_subnets\_per\_env](#input\_amt\_asg\_subnets\_per\_env) | Amount of subnets for each autoscaling service under project environments | `number` | `2` | no |
| <a name="input_amt_aws_batch_subnets_per_env"></a> [amt\_aws\_batch\_subnets\_per\_env](#input\_amt\_aws\_batch\_subnets\_per\_env) | Amount of subnets for each aws batch service under project environments | `number` | `2` | no |
| <a name="input_amt_reserved_subnets_per_env"></a> [amt\_reserved\_subnets\_per\_env](#input\_amt\_reserved\_subnets\_per\_env) | Amount of reserved subnets under project environments | `number` | `1` | no |
| <a name="input_environments"></a> [environments](#input\_environments) | Environments used in project | `list(string)` | <pre>[<br>  "test",<br>  "ua_test",<br>  "prod"<br>]</pre> | no |
| <a name="input_tags"></a> [tags](#input\_tags) | Tags set to VPC | `map(string)` | <pre>{<br>  "project_name": "research-kedro-microservice",<br>  "region": "us-east-2"<br>}</pre> | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_amt_asg_subnets_per_env"></a> [amt\_asg\_subnets\_per\_env](#output\_amt\_asg\_subnets\_per\_env) | Amount of subnets for each autoscaling service under project environments |
| <a name="output_amt_aws_batch_subnets_per_env"></a> [amt\_aws\_batch\_subnets\_per\_env](#output\_amt\_aws\_batch\_subnets\_per\_env) | Amount of subnets for each aws batch service under project environments |
| <a name="output_amt_reserved_subnets_per_env"></a> [amt\_reserved\_subnets\_per\_env](#output\_amt\_reserved\_subnets\_per\_env) | Amount of reserved subnets under project environments |
| <a name="output_asg_subnets_cidr"></a> [asg\_subnets\_cidr](#output\_asg\_subnets\_cidr) | CIDR blocks of asg subnets |
| <a name="output_aws_batch_subnets_cidr"></a> [aws\_batch\_subnets\_cidr](#output\_aws\_batch\_subnets\_cidr) | CIDR blocks of aws batch subnets |
| <a name="output_cidr_end_octect_asg"></a> [cidr\_end\_octect\_asg](#output\_cidr\_end\_octect\_asg) | CIDR ending octect value for auto-scaling subnet |
| <a name="output_cidr_end_octect_aws_batch"></a> [cidr\_end\_octect\_aws\_batch](#output\_cidr\_end\_octect\_aws\_batch) | CIDR ending octect value for aws batch subnet |
| <a name="output_cidr_end_octect_reserved"></a> [cidr\_end\_octect\_reserved](#output\_cidr\_end\_octect\_reserved) | CIDR ending octect value for reserved subnet |
| <a name="output_cidr_start_octect_asg"></a> [cidr\_start\_octect\_asg](#output\_cidr\_start\_octect\_asg) | CIDR starting octect value for auto-scaling subnet |
| <a name="output_cidr_start_octect_aws_batch"></a> [cidr\_start\_octect\_aws\_batch](#output\_cidr\_start\_octect\_aws\_batch) | CIDR starting octect value for aws batch subnet |
| <a name="output_cidr_start_octect_reserved"></a> [cidr\_start\_octect\_reserved](#output\_cidr\_start\_octect\_reserved) | CIDR starting octect value for reserved subnet |
| <a name="output_default_vpc_cidr_block"></a> [default\_vpc\_cidr\_block](#output\_default\_vpc\_cidr\_block) | The CIDR block of the Default VPC |
| <a name="output_default_vpc_default_security_group_id"></a> [default\_vpc\_default\_security\_group\_id](#output\_default\_vpc\_default\_security\_group\_id) | Default security group name |
| <a name="output_environments"></a> [environments](#output\_environments) | Environments used in project |
| <a name="output_n_asg_subnets"></a> [n\_asg\_subnets](#output\_n\_asg\_subnets) | Total amount of asg subnets created under VPC for all environments |
| <a name="output_n_aws_batch_subnets"></a> [n\_aws\_batch\_subnets](#output\_n\_aws\_batch\_subnets) | Total amount of aws batch subnets created under VPC for all environments |
| <a name="output_n_reserved_subnets"></a> [n\_reserved\_subnets](#output\_n\_reserved\_subnets) | Total amount of reserved subnets created under VPC for all environments |
| <a name="output_n_total_subnets"></a> [n\_total\_subnets](#output\_n\_total\_subnets) | Total amount of subnets created under VPC for all environments |
| <a name="output_reserved_subnets_cidr"></a> [reserved\_subnets\_cidr](#output\_reserved\_subnets\_cidr) | CIDR blocks of reserved subnets |
| <a name="output_tags"></a> [tags](#output\_tags) | Tags assigned to project |
| <a name="output_vpc_cidr_block"></a> [vpc\_cidr\_block](#output\_vpc\_cidr\_block) | VPC CIDR blocks |
| <a name="output_vpc_id"></a> [vpc\_id](#output\_vpc\_id) | VPC id |
<!-- END_TF_DOCS -->
