resource "aws_subnet" "public-basic-arch-subnet" {
  vpc_id     = aws_vpc.main-basic-arch-vpc.id
  cidr_block = "10.0.0.0/24"

  tags = {
    Name = "basic-arch-public"
  }
}

resource "aws_subnet" "private-basic-arch-subnet" {
  vpc_id     = aws_vpc.main-basic-arch-vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "basic-arch-private"
  }
}
