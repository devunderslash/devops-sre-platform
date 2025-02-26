resource "aws_instance" "public-web-instance" {
  ami                         = "ami-04681163a08179f28"
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public-basic-arch-subnet.id
  key_name                    = aws_key_pair.basic-arch-generated_key.key_name
  associate_public_ip_address = true
  security_groups             = [aws_security_group.basic-arch-public-sg.id]

  tags = {
    Name = "basic-arch-public-web"
  }
}

resource "aws_instance" "private-web-instance" {
  ami                         = "ami-04681163a08179f28"
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.private-basic-arch-subnet.id
  key_name                    = aws_key_pair.basic-arch-generated_key.key_name
  associate_public_ip_address = false
  security_groups             = [aws_security_group.basic-arch-private-sg.id]
  user_data = <<EOF
    #!/bin/bash
    cd /home/var
    sudo apt-get update
    sudo apt-get install python3-pip -y
    sudo pip3 install ansible
    sleep 30
    cd /home/var/opt
    git clone https://github.com/devunderslash/devops-sre-platform.git
EOF

  tags = {
    Name = "basic-arch-private-web"
  }
}

# Install python onto the ec2 instance with remote provisioner
# Tested, this works if needed.

# resource "null_resource" "install_python" {
#   provisioner "remote-exec" {
#     inline = [
#       "sudo yum install -y python3"
#     ]
#     connection {
#       type        = "ssh"
#       user        = "ec2-user"
#       # private key is in the same directory as this file
#       private_key = file("aws-basic-arch-keypair.pem")
#       host        = aws_instance.public-web-instance.public_ip
#     }
#   }
# }


# *** Can't install python onto the private instance as it doesn't have ssh key on initial setup ***

# Install python onto the ec2 instance with remote provisioner
# resource "null_resource" "install_python_private" {
#   provisioner "remote-exec" {
#     inline = [
#       "sudo yum install -y python3"
#     ]

#     connection {
#       type        = "ssh"
#       user        = "ec2-user"
#       private_key = file("aws-basic-arch-keypair.pem")
#       host        = aws_instance.private-web-instance.private_ip
#     }
#   }
# }


