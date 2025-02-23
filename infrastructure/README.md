# Infrastructure as Code

This repository contains the infrastructure as code (Terraform) for the following for the following:
- Three tier architecture on AWS
- Small EKS cluster
- Lightsail instance

## Pre-Requisites

- Terraform
- AWS CLI

## Setup

- AWS Configure
- S3 Bucket to store Terraform state (optional)

Make sure that you have setup an AWS account and have added a user with programmatic access. You will need to generate an access key and secret key for this user. With the access key and secret key, you will need to configure the AWS CLI with the following command:

```bash
aws configure
```

You will need to enter the access key and secret key when prompted. You will also need to enter the default region and output format.

You can also setup an S3 bucket to store the Terraform state. This is optional but recommended for production workloads. You can create an S3 bucket with the following command:

```bash
aws s3api create-bucket --bucket my-terraform-state-bucket --region us-east-1
```

You can then enable versioning on the bucket with the following command:

```bash
aws s3api put-bucket-versioning --bucket my-terraform-state-bucket --versioning-configuration Status=Enabled
```

**Note**: You will need to replace `my-terraform-state-bucket` with your own bucket name. Make sure that the bucket name is globally unique or else you will get the following error:

```
An error occurred (BucketAlreadyExists) when calling the CreateBucket operation: The requested bucket name is not available. The bucket namespace is shared by all users of the system. Please select a different name and try again.
```

## Usage

To deploy the infrastructure, you will need to run the following commands:

```bash
cd infrastructure/<infra-type>
terraform init
terraform plan
terraform apply
```

You will need to replace `<infra-type>` with the infrastructure type you want to deploy. You can choose from `three-tier`, `eks`, or `lightsail`.

You will need to enter `yes` when prompted to deploy the infrastructure.


## Resources
- [ECS Networking](https://section411.com/2019/07/hello-world/)
- [Native s3 Locking](https://rafaelmedeiros94.medium.com/goodbye-dynamodb-terraform-s3-backend-now-supports-native-locking-06f74037ad39)
- [Deploying container from local docker](https://erik-ekberg.medium.com/terraform-ecs-fargate-example-1397d3ab7f02)
- [Structuring Terraform Projects](https://spacelift.io/blog/terraform-files#best-practices-for-structuring-terraform-projects)

Quick Info Articles on AWS:
- [ASGs and NACLs](https://medium.com/awesome-cloud/aws-difference-between-security-groups-and-network-acls-adc632ea29ae)
- [IGW and NAT Gateway](https://medium.com/awesome-cloud/aws-vpc-difference-between-internet-gateway-and-nat-gateway-c9177e710af6)
- [ALB and NLB](https://medium.com/awesome-cloud/aws-difference-between-application-load-balancer-and-network-load-balancer-cb8b6cd296a4)
- [EKS and ECS](https://medium.com/awesome-cloud/aws-amazon-eks-vs-amazon-ecs-comparison-difference-between-eks-and-ecs-7451abd23859)
- [SQS and SNS](https://medium.com/awesome-cloud/aws-difference-between-sqs-and-sns-61a397bf76c5)
- [Aurora and RDS](https://medium.com/awesome-cloud/aws-difference-between-amazon-aurora-and-amazon-rds-comparison-aws-aurora-vs-aws-rds-databases-60a69dbec41f)
- [Parameter Store and Secrets Manager](https://medium.com/awesome-cloud/aws-difference-between-secrets-manager-and-parameter-store-systems-manager-f02686604eae)
