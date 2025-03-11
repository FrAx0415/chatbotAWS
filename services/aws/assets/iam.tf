resource "aws_iam_policy" "policy_monitoring_resources" {
  name = "policy_monitoring_resources"
  path = "/"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "elasticache:DescribeReplicationGroups",
          "elasticache:DescribeUpdateActions",
          "elasticache:DescribeCacheClusters"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeInstanceStatus"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "cloudwatch:GetMetricData",
          "cloudwatch:DescribeAlarms",
          "cloudwatch:GetMetricStatistics"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "attach_policy_monitoring_resources" {
  name       = "attach_policy_monitoring_resources"
  users      = ["a.valas"]
  policy_arn = aws_iam_policy.policy_monitoring_resources.arn
}
############# EC2 SSM ROLE
resource "aws_iam_role" "ec2_ssm_role" {
  name = "ec2_ssm_role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}
