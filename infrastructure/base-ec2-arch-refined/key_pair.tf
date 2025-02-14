resource "tls_private_key" "pri-key-basic-arch" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "basic-arch-generated_key" {
  key_name   = var.generated_key_name
  public_key = tls_private_key.pri-key-basic-arch.public_key_openssh

  provisioner "local-exec" {
    command = <<-EOT
      echo '${tls_private_key.pri-key-basic-arch.private_key_pem}' > ./'${var.generated_key_name}'.pem
      chmod 400 ./'${var.generated_key_name}'.pem
    EOT
  }
}
