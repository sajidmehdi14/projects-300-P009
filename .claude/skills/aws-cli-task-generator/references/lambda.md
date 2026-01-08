# Lambda Command Patterns

## Create Function (Python)

```bash
# Package code first
zip function.zip lambda_function.py

# Create function
aws lambda create-function \
  --function-name <function-name> \
  --runtime python3.11 \
  --role <iam-role-arn> \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables={KEY1=value1,KEY2=value2} \
  --tags Environment=prod,Owner=devops
```

## Update Function Code

```bash
aws lambda update-function-code \
  --function-name <function-name> \
  --zip-file fileb://function.zip
```

## Update Function Configuration

```bash
aws lambda update-function-configuration \
  --function-name <function-name> \
  --timeout 60 \
  --memory-size 1024 \
  --environment Variables={KEY1=newvalue}
```

## Invoke Function

```bash
# Synchronous
aws lambda invoke \
  --function-name <function-name> \
  --payload '{"key": "value"}' \
  response.json

# Asynchronous
aws lambda invoke \
  --function-name <function-name> \
  --invocation-type Event \
  --payload '{"key": "value"}' \
  response.json
```

## Common Runtimes

- Python: `python3.11`, `python3.10`, `python3.9`
- Node.js: `nodejs20.x`, `nodejs18.x`
- Java: `java21`, `java17`, `java11`
- .NET: `dotnet8`, `dotnet6`
- Go: `provided.al2023`
- Ruby: `ruby3.2`

## VPC Configuration (Optional)

```bash
aws lambda update-function-configuration \
  --function-name <function-name> \
  --vpc-config SubnetIds=<subnet-id-1>,<subnet-id-2>,SecurityGroupIds=<sg-id>
```

## Enable X-Ray Tracing

```bash
aws lambda update-function-configuration \
  --function-name <function-name> \
  --tracing-config Mode=Active
```

## Cleanup Commands

```bash
# Delete function
aws lambda delete-function --function-name <function-name>
```

## IAM Role for Lambda (Basic)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Attach managed policy: `arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole`

## IAM Permissions for Creating Lambda

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:CreateFunction",
        "lambda:DeleteFunction",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "lambda:InvokeFunction",
        "lambda:GetFunction",
        "lambda:ListFunctions"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "<lambda-execution-role-arn>"
    }
  ]
}
```
