# Public subnet route table and association
resource "aws_route_table" "basic-arch-public-rt" {
  vpc_id = aws_vpc.main-basic-arch-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.basic-arch-igw.id
  }

  tags = {
    Name = "basic-arch-public-rt"
  }
}

resource "aws_route_table_association" "public-basic-arch-rt-assoc" {
  subnet_id      = aws_subnet.public-basic-arch-subnet.id
  route_table_id = aws_route_table.basic-arch-public-rt.id
}

# Private subnet route table and association
resource "aws_route_table" "basic-arch-private-rt" {
  vpc_id = aws_vpc.main-basic-arch-vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.basic-arch-ngw.id
  }

  tags = {
    Name = "basic-arch-private-rt"
  }
}

resource "aws_route_table_association" "private-basic-arch-rt-assoc" {
  subnet_id      = aws_subnet.private-basic-arch-subnet.id
  route_table_id = aws_route_table.basic-arch-private-rt.id
}
