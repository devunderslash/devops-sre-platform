# Basic ECS Fargate Infrastructure with SSM Param Store intergration
This module creates a basic ECS Fargate infrastructure with SSM Param Store integration.

## Pre-Requisites
- Terraform
- AWS CLI
- AWS Account
- Docker

## Paramater Store
First set the following params in AWS Param Store for a working example:
```bash
aws ssm put-parameter --name "/devops-sre-platform/ecs-fargate/SECRET_KEY" --value "SECRET_KEY=nada" --type "SecureString"
aws ssm put-parameter --name "/devops-sre-platform/ecs-fargate/DATABASE_URL" --value "DATABASE_URL=sqlite:///your_database.db" --type "SecureString"
aws ssm put-parameter --name "/devops-sre-platform/ecs-fargate/SQLALCHEMY_DATABASE_URI" --value "SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3" --type "SecureString"
aws ssm put-parameter --name "/devops-sre-platform/ecs-fargate/SQLALCHEMY_TRACK_MODIFICATIONS" --value "SQLALCHEMY_TRACK_MODIFICATIONS=False" --type "String"
aws ssm put-parameter --name "/devops-sre-platform/ecs-fargate/SQLALCHEMY_ENGINE_OPTIONS" --value "SQLALCHEMY_ENGINE_OPTIONS={'pool_size': 10,'pool_recycle': 60,'pool_pre_ping': True}" --type "String"
```

Confirm the params are set:
```bash
aws ssm get-parameter --name "/devops-sre-platform/ecs-fargate/SECRET_KEY" --query Parameter.Value --output text
# For secret values
aws ssm get-parameter --name "/devops-sre-platform/ecs-fargate/SQLALCHEMY_DATABASE_URI" --with-decryption --query Parameter.Value --output text
```

## Create Image
Use the README from the containerization directory to create an image from the backend code in the repository for use with this infrastructure. Or just drop to the root directory and run the following:
```bash
docker build -f containerization/Dockerfile.backend -t backend .
```

This will give you the image to run all of the next steps.

## Push image to ECR 
```bash
- aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 755952485507.dkr.ecr.us-east-1.amazonaws.com
# - create the ECR repo
- aws ecr create-repository --repository-name backend-ecs-example/backend
# Tag prebuilt image 'backend' with the ECR repo
- docker tag backend:latest 755952485507.dkr.ecr.us-east-1.amazonaws.com/backend-ecs-example/backend:latest
# Push the image to ECR
- docker push 755952485507.dkr.ecr.us-east-1.amazonaws.com/backend-ecs-example/backend:latest
```

## Running the Infrastructure
```bash
cd infrastructure/ecs-fargate
terraform init
terraform plan
terraform apply
```

## Destroying the Infrastructure
```bash
terraform destroy
```

## Outputs
- 'load balancer dns name' - The DNS name of the load balancer


## Test the application
```bash
curl -X POST <load balancer output>/api/players -d '{"id": "1", "name": "John Doe", "dob": "2000-05-15", "joined_group_date": "2023-01-06"}' -H "Content-Type: application/json"

curl -X GET <load balancer output>/api/players
```


## Resource

- [ECS Provider](https://registry.terraform.io/modules/terraform-aws-modules/ecs/aws/latest)

- [In Depth ECS article](https://erik-ekberg.medium.com/terraform-ecs-fargate-example-1397d3ab7f02)