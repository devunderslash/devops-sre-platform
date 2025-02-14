resource "aws_eip" "basic-arch-ngw-eip" {
  domain = "vpc"
}

resource "aws_nat_gateway" "basic-arch-ngw" {
  allocation_id     = aws_eip.basic-arch-ngw-eip.id
  subnet_id         = aws_subnet.public-basic-arch-subnet.id
  connectivity_type = "public"

  tags = {
    Name = "basic-arch-ngw"
  }
}