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
| <a name="module_ec2"></a> [ec2](#module\_ec2) | terraform-aws-modules/ec2-instance/aws | = 3.5.0 |
| <a name="module_elk_sg"></a> [elk\_sg](#module\_elk\_sg) | terraform-aws-modules/security-group/aws | ~> 4.0 |

## Resources

| Name | Type |
|------|------|
| [aws_eip_association.elk_eip](https://registry.terraform.io/providers/hashicorp/aws/4.9.0/docs/resources/eip_association) | resource |
| [aws_network_interface.elk](https://registry.terraform.io/providers/hashicorp/aws/4.9.0/docs/resources/network_interface) | resource |
| [aws_ami.ubuntu](https://registry.terraform.io/providers/hashicorp/aws/4.9.0/docs/data-sources/ami) | data source |
| [aws_subnet.reserved_subnets_id](https://registry.terraform.io/providers/hashicorp/aws/4.9.0/docs/data-sources/subnet) | data source |
| [terraform_remote_state.aws_eip](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.vpc](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_instance_type"></a> [instance\_type](#input\_instance\_type) | Default instance type for proxy instance | `string` | `"t2.micro"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_ami"></a> [ami](#output\_ami) | AMI assinged to proxy instances |
| <a name="output_reserved_aws_subnets_id"></a> [reserved\_aws\_subnets\_id](#output\_reserved\_aws\_subnets\_id) | Reserved subnets id |
<!-- END_TF_DOCS -->
