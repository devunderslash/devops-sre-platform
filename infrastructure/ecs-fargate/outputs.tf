# Output the URL of the ALB
output "url" { value = "http://${module.alb.lb_dns_name}" }