provider "aws" {
  profile = "default"
  region = "us-east-1"
}

/*
terraform/main.tf contains only resources strictly
related to deploying the application in ECS
*/

# create the ECS cluster
resource "aws_ecs_cluster" "fp-ecs-cluster" {
  name = "flask-app"

  tags = {
    Name = "flask-app"
  }
}

# create and define the container task
resource "aws_ecs_task_definition" "fp-ecs-task" {
  family = "flask-app"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = "256"
  memory = "512"
  execution_role_arn = aws_iam_role.ecs_tasks_execution_role.arn
  container_definitions = <<DEFINITION
[
   {
      "name":"flask-app",
      "image":"${var.flask_app_image}",
      "essential":true,
      "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
         "awslogs-group": "ecs-logs",
         "awslogs-region": "us-east-1",
         "awslogs-stream-prefix": "ecs-demo-app"
         }
      },
      "portMappings":[
         {
            "containerPort":5000,
            "hostPort":5000,
            "protocol":"tcp"
         }
      ]
   }
]
DEFINITION
}


resource "aws_ecs_service" "flask-service" {
  name = "flask-app-service"
  cluster = aws_ecs_cluster.fp-ecs-cluster.id
  task_definition = aws_ecs_task_definition.fp-ecs-task.arn
  desired_count = 2
  launch_type = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.fp-ecs-sg.id]
    subnets = aws_subnet.fp-public-subnets.*.id
    assign_public_ip = true
  }

  load_balancer {
    container_name = "flask-app"
    container_port = var.flask_app_port
    target_group_arn = aws_alb_target_group.fp-target-group.id
  }

  depends_on = [
    aws_alb_listener.fp-alb-listener
  ]
}
