output "public_instance_ip" {
  value = aws_instance.public-web-instance.public_ip
}

output "private_instance_ip" {
  value = aws_instance.private-web-instance.private_ip
}