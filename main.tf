terraform {
  backend "s3" {
    bucket = "testchatbot777-281670075220"
    region = "eu-central-1"
    key = "ec2-example/terraform.tfstate"
    dynamodb_table = "terraform-lock"
    encrypt = true
  }
}

