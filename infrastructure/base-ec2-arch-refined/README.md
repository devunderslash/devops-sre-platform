# Basic EC2 Architecture Refined
This takes the infrastructure laid out in the basic-ec2-arch and refines it into more managaable modules. This is a good starting point for a more complex architecture.

## Diagram
![Basic EC2 Architecture](../basic-ec2-arch.png)

## Pre-Requisites
- AWS Account
- `default` profile setup locally in /.aws/credentials
- Terraform

# Basic ec2 Architecture
This is a basic ec2 architecture that can be used as a starting point for your infrastructure. It includes a VPC, a public subnet, a private subnet, an internet gateway, route tables(public/private), security groups(public/private) and Amazon EC2 ami's in both subnets.

## Diagram
![Basic EC2 Architecture](../basic-ec2-arch.png)

## Pre-Requisites
- AWS Account
- Terraform

## Installation
1. Clone the repository
2. Change directory to the infrastructure/base-ec2-arch-refined directory
3. Run the following commands:
```bash
terraform init
terraform plan
terraform apply
```
* NOTE - For a more readable format of the plan output, you can run the following command:
```bash
terraform plan -no-color >> output.txt
```
4. The output will show the public and private IP addresses of the EC2 instances.


## Accessing the EC2 Instances
Once the terraform runs it copies the key to this directory with the name 'aws-basic-arch-keypair.pem'. You should also be able to retrieve the public and private IP addresses of the EC2 instances as they will output after the terraform apply command.

What we want to do next is to copy the private key to the public instance so that wer can confirm that we can access the private instance from the public instance.

Copy the private key to the infrastructure/base-ec2-arch directory and run the following command:
```bash
scp -i aws-basic-arch-keypair.pem aws-basic-arch-keypair.pem ec2-user@<public-ip>:/home/ec2-user/
```
Now ssh into the public instance:
```bash
ssh -i aws-basic-arch-keypair.pem ec2-user@<public-ip>
```
Now ssh into the private instance from the public instance:
```bash
ssh -i aws-basic-arch-keypair.pem ec2-user@<private-ip>
```

## Destroying the Infrastructure
To destroy the infrastructure, run the following command:
```bash
terraform destroy
```

## Resources

This architecture was created whilst following along with the following youtube video:
[AWS Networking Basics For Programmers](https://www.youtube.com/watch?v=2doSoMN2xvI)

Terraform Provider for AWS
https://registry.terraform.io/providers/hashicorp/aws/latest/docs
