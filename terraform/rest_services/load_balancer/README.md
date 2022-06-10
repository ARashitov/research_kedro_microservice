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
| <a name="module_alb"></a> [alb](#module\_alb) | terraform-aws-modules/alb/aws | = 6.4.0 |
| <a name="module_alb_sg"></a> [alb\_sg](#module\_alb\_sg) | terraform-aws-modules/security-group/aws | = 4.9.0 |

## Resources

| Name | Type |
|------|------|
| [aws_subnet.asg_subnets_cidr](https://registry.terraform.io/providers/hashicorp/aws/4.9.0/docs/data-sources/subnet) | data source |
| [terraform_remote_state.vpc](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

No inputs.

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_asg_env_subnets_ids"></a> [asg\_env\_subnets\_ids](#output\_asg\_env\_subnets\_ids) | n/a |
| <a name="output_asg_subnets_cidr"></a> [asg\_subnets\_cidr](#output\_asg\_subnets\_cidr) | n/a |
| <a name="output_asg_subnets_ids"></a> [asg\_subnets\_ids](#output\_asg\_subnets\_ids) | n/a |
| <a name="output_env"></a> [env](#output\_env) | n/a |
| <a name="output_env_idx"></a> [env\_idx](#output\_env\_idx) | n/a |
| <a name="output_subnet_idx_end_env"></a> [subnet\_idx\_end\_env](#output\_subnet\_idx\_end\_env) | n/a |
| <a name="output_subnet_idx_start_env"></a> [subnet\_idx\_start\_env](#output\_subnet\_idx\_start\_env) | n/a |
<!-- END_TF_DOCS -->
