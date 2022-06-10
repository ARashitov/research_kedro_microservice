<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0.8 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | = 4.9.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_terraform"></a> [terraform](#provider\_terraform) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_ec2"></a> [ec2](#module\_ec2) | terraform-aws-modules/ec2-instance/aws | = 3.5.0 |
| <a name="module_elk_sg"></a> [elk\_sg](#module\_elk\_sg) | terraform-aws-modules/security-group/aws | ~> 4.0 |

## Resources

| Name | Type |
|------|------|
| [terraform_remote_state.vpc](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_ami"></a> [ami](#input\_ami) | The AMI from which to launch the instance | `string` | `"ami-08be45d446b4d01f1"` | no |
| <a name="input_instance_type"></a> [instance\_type](#input\_instance\_type) | Default instance type for proxy instance | `string` | `"c5a.large"` | no |
| <a name="input_key_name"></a> [key\_name](#input\_key\_name) | Key name | `string` | `"aws-us-east-1"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_public_ip"></a> [public\_ip](#output\_public\_ip) | The public IP address assigned to the instance, if applicable. NOTE: If you are using an aws\_eip with your instance, you should refer to the EIP's address directly and not use `public_ip` as this field will change after the EIP is attached. |
<!-- END_TF_DOCS -->
