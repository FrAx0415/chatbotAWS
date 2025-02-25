resource "aws_lambda_function" "chatbot-lambda" {
  function_name = "chatbot-lambda"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_hello_world.key

  runtime = "python 3.11"
  handler = "chatbot-lambda.lambda_handler"

  source_code_hash = data.archive_file.lambda_hello_world.output_base64sha256

  role = aws_iam_role.lambda_exec.arn
}

resource "aws_cloudwatch_log_group" "chatbot-lambda" {
  name = "/aws/lambda/${aws_lambda_function.chatbot-lambda.function_name}"

  retention_in_days = 30
}

# Unified IAM Role per tutti i servizi
resource "aws_iam_role" "unified_role" {
  name = "unified-service-role"
  
  # Assume role policy che permette a multiple services di assumere questo ruolo
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = [
            "lambda.amazonaws.com",
            "apigateway.amazonaws.com",
            "bedrock.amazonaws.com",
            "opensearchservice.amazonaws.com"
          ]
        }
      }
    ]
  })
}

# Policy unificata per tutti i servizi
resource "aws_iam_role_policy" "unified_policy" {
  name = "unified-service-policy"
  role = aws_iam_role.unified_role.id
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # Logs permissions
      {
        Effect = "Allow",
        Action = "logs:CreateLogGroup",
        Resource = "arn:aws:logs:eu-central-1:281670075220:*"
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = [
          "arn:aws:logs:eu-central-1:281670075220:log-group:/aws/lambda/chatbot-connect:*",
          "arn:aws:logs:eu-central-1:281670075220:log-group:/aws/bedrock/example:*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      },
      # Bedrock permissions
      {
        Sid = "BedrockAll",
        Effect = "Allow",
        Action = "bedrock:*",
        Resource = "*"
      },
      # KMS permissions
      {
        Sid = "DescribeKey",
        Effect = "Allow",
        Action = "kms:DescribeKey",
        Resource = "arn:*:kms:*:::*"
      },
      # API and network permissions
      {
        Sid = "APIsWithAllResourceAccess",
        Effect = "Allow",
        Action = [
          "iam:ListRoles",
          "ec2:DescribeVpcs",
          "ec2:DescribeSubnets",
          "ec2:DescribeSecurityGroups"
        ],
        Resource = "*"
      },
      # SageMaker permissions for Bedrock
      {
        Sid = "MarketplaceModelEndpointMutatingAPIs",
        Effect = "Allow",
        Action = [
          "sagemaker:CreateEndpoint",
          "sagemaker:CreateEndpointConfig",
          "sagemaker:CreateModel",
          "sagemaker:DeleteEndpoint",
          "sagemaker:UpdateEndpoint"
        ],
        Resource = [
          "arn:aws:sagemaker:*:*:endpoint/*",
          "arn:aws:sagemaker:*:*:endpoint-config/*",
          "arn:aws:sagemaker:*:*:model/*"
        ],
        Condition = {
          StringEquals = {
            "aws:CalledViaLast": "bedrock.amazonaws.com",
            "aws:ResourceTag/sagemaker-sdk:bedrock": "compatible"
          }
        }
      },
      # OpenSearch permissions
      {
        Effect = "Allow",
        Action = [
          "es:ESHttpGet",
          "es:ESHttpPost",
          "es:ESHttpPut",
          "es:ESHttpDelete",
          "es:DescribeDomain",
          "es:DescribeDomains"
        ],
        Resource = "*"
      },
      # S3 permissions for Bedrock logging
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::example-bedrock-logs-*",
          "arn:aws:s3:::example-bedrock-logs-*/*"
        ]
      },
      # Lambda permissions
      {
        Effect = "Allow",
        Action = [
          "lambda:InvokeFunction"
        ],
        Resource = "*"
      }
    ]
  })
}
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
