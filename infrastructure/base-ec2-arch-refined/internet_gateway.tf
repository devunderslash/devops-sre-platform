resource "aws_internet_gateway" "basic-arch-igw" {
  vpc_id = aws_vpc.main-basic-arch-vpc.id

  tags = {
    Name = "basic-arch-igw"
  }
}