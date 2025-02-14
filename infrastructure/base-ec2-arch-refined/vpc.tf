resource "aws_vpc" "main-basic-arch-vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "basic-arch-vpc"
  }
}