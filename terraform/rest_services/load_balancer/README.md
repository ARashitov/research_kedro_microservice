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
| <a name="module_alb"></a> [alb](#module\_alb) | terraform-aws-modules/alb/aws | = 6.4.0 |
| <a name="module_alb_sg"></a> [alb\_sg](#module\_alb\_sg) | terraform-aws-modules/security-group/aws | = 4.9.0 |

## Resources

| Name | Type |
|------|------|
| [terraform_remote_state.vpc](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_ami"></a> [ami](#input\_ami) | ami-08be45d446b4d01f1 | `string` | `""` | no |
| <a name="input_instance_types"></a> [instance\_types](#input\_instance\_types) | Default instance types for different application environments | `map(string)` | <pre>{<br>  "prod": "c5a.xlarge",<br>  "test": "c5a.xlarge",<br>  "ua_test": "c5a.xlarge"<br>}</pre> | no |
| <a name="input_key_name"></a> [key\_name](#input\_key\_name) | Key name | `string` | `"aws-us-east-1"` | no |
| <a name="input_user_data"></a> [user\_data](#input\_user\_data) | Instance initialization script | `string` | `"#!/bin/bash\necho \"version: '3'\nservices:\n\n  backend_latest:\n    image: 946627858531.dkr.ecr.us-east-1.amazonaws.com/dev_alba_scl_weee:latest\n    network_mode: host\n    env_file:n      - ../.env\n    restart: always\n    command: bash -c \"\n      python3 conf/data_env_management/main.py\n      && uvicorn app.run:app --host 0.0.0.0 --port 8001 --log-config log.ini\"\n\n  backend_stable:\n    image: 946627858531.dkr.ecr.us-east-1.amazonaws.com/dev_alba_scl_weee:v1.0.5-alpha\n    network_mode: host\n    env_file:n      - ../.env\n    restart: always\n    command: bash -c \"\n      python3 conf/data_env_management/main.py\n      && uvicorn app.run:app --host 0.0.0.0 --port 8000 --log-config log.ini\"\n\n  osrm_service:\n    image: public.ecr.aws/u6u7x5n5/dev_osrm_service:1.0.0\n    environment:\n    - OSRM_PBF_URL=https://download.openstreetmap.fr/extracts/asia/china/hong_kong-latest.osm.pbfn    - OSRM_GRAPH_PROFILE_URL=https://raw.githubusercontent.com/WasteLabs/osrm_profiles/master/truck_v1.luan    - OSRM_MAX_MATCHING_SIZE=86400\n    network_mode: host\n\" > docker-compose.yaml;\nsudo docker-compose -f docker-compose.yaml up -d;\n"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lb_dns_name"></a> [lb\_dns\_name](#output\_lb\_dns\_name) | The DNS name of the load balancer. |
| <a name="output_lb_id"></a> [lb\_id](#output\_lb\_id) | The ID and ARN of the load balancer we created. |
| <a name="output_target_group_arns"></a> [target\_group\_arns](#output\_target\_group\_arns) | ARNs of the target groups. Useful for passing to your Auto Scaling group. |
<!-- END_TF_DOCS -->
