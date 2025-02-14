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

  tags = {
    Name = "basic-arch-private-web"
  }
}
