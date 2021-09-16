# Flask Microservice App Stipe API

This is a micro-service that handles Stripe payments, written in Python.

#  How To Use?
## Dependencies
This app has dependencies or requirements in order to successfully deliver the desired state. These dependencies include the following:

-   An AWS account is required
-   An execution role or IAM key is required for authentication with the AWS account
-   An Elastic Container Repository containing the reference image

## Configuration
Navigate to the `src` directory and rename **config.py.example** file to **config.py** and replace required values / keys details

## Application build

 1. First, you will need to create an ECR repository. Run the following AWS CLI command from your terminal
 `aws ecr create-repository \ --repository-name flask-docker-stripe-app \ --image-scanning-configuration scanOnPush=true \ --region us-east-1`

 2. In the AWS Console, open **Services**, **Elastic Container Registry**. Select the **flask-docker-stripe-app**

 3. Now, log into ECR from the command line. Run the following command
`aws ecr get-login-password --region us-east-1  | docker login --username AWS --password-stdin <AWS_ID>.dkr.ecr.us-east-1.amazonaws.com/flask-docker-demo-app`

 4. Navigate to the root of the repository and run:
`cd src `
5. Run the following image to build the Docker image:
`docker build --tag flask-docker-stripe-app .`
6. Run the following command to tag the Docker image and make sure to update the command with your account ID:
   `docker tag flask-docker-demo-app:latest <AWS_ID>.dkr.ecr.us-east-1.amazonaws.com/flask-docker-stripe-app:latest`
7. You will now push your newly created Docker image to ECR. Run the following command to deploy the image to ECR:
`docker push <AWS_ID>.dkr.ecr.us-east-1.amazonaws.com/flask-docker-stripe-app:latest`

You can also verify and retrieve the URI for the image repository in the AWS console. Open **Services**, **Elastic Container Registry**, **Repositories**. Select the **flask-docker-demo-app** repository.

## Deploy Application using Terraform
### Terraform directory structure / details
-   **config.tf**: This file contains the Terraform provider and AWS module version constraints or requirements. Other provider information can be passed here. The AWS Region is specified here for the purpose of this article.
-   **data.tf**: This file acts as a data handler. It retrieves specific information for later use by other resources.
-   **main.tf**: This is the main execution file.
-   **outputs.tf**: This file contains outputs to be passed to the shell during execution that are also made available to other modules at runtime.
-   **variables.tf**: This file provides input variables for the Terraform configuration.

**use latest terraform** for installation [read](https://learn.hashicorp.com/tutorials/terraform/install-cli)
1. Navigate to Terraform directory
`cd terraform`
2. run a Terraform plan , execute the following command from the root module directory
`terraform plan`
### Deployment
To run a `terraform apply`, execute the following command from the root terraform directory:
`terraform apply`

When the process completes, you will receive the following message:

```python
Apply complete! Resources: 47 added, 0 changed, 0 destroyed.

Outputs:

alb_dns_name = "ecsalb-2126701046.us-east-1.elb.amazonaws.com"
```

Retrieve the DNS name for the load balancer from the _alb_dns_name_ output seen above. Navigate to this address in your web browser.

### Database
As we are currently using sqlite3 DB
if you need Demo user name password use below remeber once user subscribe he/she can't get another chance to subscribe

username demo : amardesai@ve.com
password : amar12345