provider "aws" {
  profile = "default"
  region = "eu-west-2"
}

/*
terraform/main.tf contains only resources strictly
related to deploying the application in ECS
*/

# create the ECS cluster
resource "aws_ecs_cluster" "flask-mywallst-app" {
  name = "flask-mywallst-app"
}

# create and define the container task
resource "aws_ecs_task_definition" "flask-mywallst-task" {
  family                   = "flask-mywallst-task" # Naming our first task
  container_definitions    = <<DEFINITION
  [
    {
      "name": "flask-mywallst-task",
      "image": "${var.flask_app_image}",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000
        }
      ],
      "memory": 512,
      "cpu": 256
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"] # Stating that we are using ECS Fargate
  network_mode             = "awsvpc"    # Using awsvpc as our network mode as this is required for Fargate
  memory                   = 512         # Specifying the memory our container requires
  cpu                      = 256         # Specifying the CPU our container requires
  execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole.arn}"
}

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role_policy.json}"
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = "${aws_iam_role.ecsTaskExecutionRole.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

#creating the service
resource "aws_ecs_service" "mywallst-flask-service" {
  name            = "mywallst-flask-service"                               # Naming our first service
  cluster         = "${aws_ecs_cluster.flask-mywallst-app.id}"             # Referencing our created Cluster
  task_definition = "${aws_ecs_task_definition.flask-mywallst-task.arn}"   # Referencing the task our service will spin up
  launch_type     = "FARGATE"
  desired_count   = 2 # Setting the number of containers we want deployed to 3

  network_configuration {
    subnets          = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}", "${aws_default_subnet.default_subnet_c.id}"]
    assign_public_ip = true # Providing our containers with public IPs
  }


}

# resource "aws_ecs_service" "flask-service" {
#   name = "flask-app-service"
#   cluster = aws_ecs_cluster.fp-ecs-cluster.id
#   task_definition = aws_ecs_task_definition.fp-ecs-task.arn
#   desired_count = 2
#   launch_type = "FARGATE"

#   network_configuration {
#     security_groups = [aws_security_group.fp-ecs-sg.id]
#     subnets = aws_subnet.fp-public-subnets.*.id
#     assign_public_ip = true
#   }

#   load_balancer {
#     container_name = "flask-app"
#     container_port = var.flask_app_port
#     target_group_arn = aws_alb_target_group.fp-target-group.id
#   }

#   depends_on = [
#     aws_alb_listener.fp-alb-listener
#   ]
# }
