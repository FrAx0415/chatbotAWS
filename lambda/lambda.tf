resource "aws_lambda_function" "chatbot_lambda" {
  function_name = "chatbot-lambda"
  runtime       = "python3.11"
  handler       = "chatbot_lambda.lambda_handler"
  filename      = "chatbot-lambda.zip"
  source_code_hash = data.archive_file.lambda_package.output_base64sha256
  role          = aws_iam_role.role_chatbot777.arn
}

resource "aws_cloudwatch_log_group" "chatbot_lambda" {
  name              = "/aws/lambda/${aws_lambda_function.chatbot_lambda.function_name}"
  retention_in_days = 30
}

resource "aws_iam_role" "role_chatbot777" {
  name = "role-chatbot777"
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

resource "aws_iam_role_policy" "unified_policy" {
  name = "unified-service-policy"
  role = aws_iam_role.role_chatbot777.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
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
      {
        Sid = "BedrockAll",
        Effect = "Allow",
        Action = "bedrock:*",
        Resource = "*"
      },
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
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::NOME_DEL_TUO_BUCKET",
          "arn:aws:s3:::NOME_DEL_TUO_BUCKET/*"
        ]
      },
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
  role       = aws_iam_role.role_chatbot777.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "archive_file" "lambda_package" {
  type        = "zip"
  source_file = "${path.module}/chatbot-lambda.zip"
  output_path = "${path.module}/chatbot-lambda.zip"
}