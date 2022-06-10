output "id" {
  value       = aws_eip.elk.id
  description = "Contains the public IP address"
}

output "public_dns" {
  value       = aws_eip.elk.public_dns
  description = "Public DNS associated with the Elastic IP address"
}

output "public_ip" {
  value       = aws_eip.elk.public_ip
  description = "The public IP address"
}
