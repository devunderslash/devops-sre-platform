provider "aws" {
  region = "us-east-1" # Feel free to change this

  default_tags {
    tags = { example = local.example }
  }
}