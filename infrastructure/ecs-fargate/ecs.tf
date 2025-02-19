module "ecs" {
  source  = "terraform-aws-modules/ecs/aws"
  version = "~> 4.1.3"

  cluster_name = local.example

  # * Allocate 20% capacity to FARGATE and then split
  # * the remaining 80% capacity 50/50 between FARGATE
  # * and FARGATE_SPOT.
  fargate_capacity_providers = {
    FARGATE = {
      default_capacity_provider_strategy = {
        base   = 20
        weight = 50
      }
    }
    FARGATE_SPOT = {
      default_capacity_provider_strategy = {
        weight = 50
      }
    }
  }
}

# Task definition
data "aws_iam_role" "ecs_task_execution_role" { name = "ecsTaskExecutionRole" }

resource "aws_ecs_task_definition" "this" {
  container_definitions = jsonencode([{
    environment : [
      { name = "SECRET_KEY", value = "secret_key" },
      { name = "DATABASE_URL", value = "sqlite:///your_database.db" },
      { name = "SQLALCHEMY_DATABASE_URI", value = "sqlite:///db.sqlite3" },
      { name = "SQLALCHEMY_TRACK_MODIFICATIONS", value = "False" },
      { name = "SQLALCHEMY_ENGINE_OPTIONS", value = "{'pool_size': 10,'pool_recycle': 60,'pool_pre_ping': True}" }
    ],
    essential    = true,
    image        = "755952485507.dkr.ecr.us-east-1.amazonaws.com/backend-ecs-example/backend:latest",
    name         = "backend",
    portMappings = [{ containerPort = local.container_port }],
  }])
  cpu                      = 256
  execution_role_arn       = data.aws_iam_role.ecs_task_execution_role.arn
  family                   = "family-of-${local.example}-tasks"
  memory                   = 512
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
}

resource "aws_ecs_service" "this" {
 cluster = module.ecs.cluster_id
 desired_count = 1
 launch_type = "FARGATE"
 name = "${local.example}-service"
 task_definition = resource.aws_ecs_task_definition.this.arn

 lifecycle {
  ignore_changes = [desired_count] # Allow external changes to happen without Terraform conflicts, particularly around auto-scaling.
 }

 load_balancer {
  container_name = local.container_name
  container_port = local.container_port
  target_group_arn = module.alb.target_group_arns[0]
 }

 network_configuration {
  security_groups = [module.vpc.default_security_group_id]
  subnets = module.vpc.private_subnets
 }
}