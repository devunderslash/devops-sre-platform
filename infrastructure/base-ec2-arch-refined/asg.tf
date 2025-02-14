resource "aws_security_group" "basic-arch-public-sg" {
  name        = "basic-arch-public-sg"
  description = "Allow SSH inbound traffic"
  vpc_id      = aws_vpc.main-basic-arch-vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "basic-arch-sg"
  }
}

resource "aws_security_group" "basic-arch-private-sg" {
  name        = "basic-arch-private-sg"
  description = "Allow SSH inbound traffic"
  vpc_id      = aws_vpc.main-basic-arch-vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "basic-arch-private-sg"
  }
}