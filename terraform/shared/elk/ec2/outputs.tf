# output "public_ip" {
#   value       = module.ec2.public_ip
#   description = "The public IP address assigned to the instance, if applicable. NOTE: If you are using an aws_eip with your instance, you should refer to the EIP's address directly and not use `public_ip` as this field will change after the EIP is attached."
# }

output "ami" {
  value       = data.aws_ami.ubuntu.id
  description = "AMI assinged to proxy instances"
}

# output "reserved_aws_subnets" {
#   value       = data.aws_subnet.reserved_subnets_id
#   description = "Reserved subnets"
# }

output "reserved_aws_subnets_id" {
  value       = local.reserved_subnet_ids
  description = "Reserved subnets id"
}
