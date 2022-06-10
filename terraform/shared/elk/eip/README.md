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

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_eip.elk](https://registry.terraform.io/providers/hashicorp/aws/4.9.0/docs/resources/eip) | resource |
| [terraform_remote_state.vpc](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

No inputs.

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_id"></a> [id](#output\_id) | Contains the public IP address |
| <a name="output_public_dns"></a> [public\_dns](#output\_public\_dns) | Public DNS associated with the Elastic IP address |
| <a name="output_public_ip"></a> [public\_ip](#output\_public\_ip) | The public IP address |
<!-- END_TF_DOCS -->
