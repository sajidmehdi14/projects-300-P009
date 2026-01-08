---
name: aws-cli-task-generator
description: Generate production-ready AWS CLI commands from natural language operations requests. Use when users describe AWS infrastructure needs in plain English (e.g., "create an EC2 instance", "set up an S3 bucket", "deploy a Lambda function"). Outputs complete commands with best-practice flags, proper tagging, IAM permissions, dry-run options, and cleanup commands. Supports EC2, S3, Lambda, RDS, and other core AWS services.
---

# AWS CLI Task Generator

Generate production-ready AWS CLI commands from natural language operations requests with best-practice flags, comprehensive tagging, and complete IAM permission documentation.

## Overview

Transform plain-English AWS infrastructure requests into executable CLI commands that follow AWS best practices. Each generated command includes:

- Complete, executable AWS CLI syntax
- Region and profile specification
- Production-grade resource tagging
- Dry-run validation commands (when supported)
- Cleanup/teardown commands
- Required IAM permissions with example policies

## Quick Start

**Input format:** Describe what you want to create in natural language.

**Examples:**
- "Create an EC2 t3.micro instance in us-east-1 with Amazon Linux 2"
- "Set up an S3 bucket with encryption and versioning"
- "Deploy a Python Lambda function with 512MB memory"
- "Launch a PostgreSQL RDS database in a private subnet"

**Output includes:**
1. Primary command with all required parameters
2. Dry-run command for validation (when available)
3. Cleanup commands for resource removal
4. IAM permissions needed to execute

## Command Generation Workflow

### Step 1: Identify the Service

Determine which AWS service the request targets:
- Compute: EC2, Lambda, ECS
- Storage: S3, EBS, EFS
- Database: RDS, DynamoDB, Aurora
- Networking: VPC, ALB, NLB, CloudFront

### Step 2: Lookup Service Patterns

Reference the appropriate service guide:
- **EC2**: See [references/ec2.md](references/ec2.md)
- **S3**: See [references/s3.md](references/s3.md)
- **Lambda**: See [references/lambda.md](references/lambda.md)
- **RDS**: See [references/rds.md](references/rds.md)

Each reference contains:
- Command templates
- Common configurations
- Instance/resource types
- Service-specific IAM permissions

### Step 3: Apply Best Practices

Reference [references/best-practices.md](references/best-practices.md) for:
- Standard tagging requirements
- Security configurations
- Cost optimization settings
- Naming conventions
- Error handling patterns

### Step 4: Generate Complete Output

Provide a structured response with all four components:

1. **Primary Command** - Full AWS CLI command
2. **Dry-Run Command** - Validation without execution
3. **Cleanup Commands** - Resource removal steps
4. **IAM Permissions** - Policy document

## Output Format

Structure your response as follows:

```markdown
### 1. Primary Command

[Complete AWS CLI command with all parameters, formatted for readability]

### 2. Dry-Run Command (if supported)

[Same command with --dry-run flag for validation]

### 3. Cleanup Commands

[Commands to remove created resources, in proper order]

### 4. Required IAM Permissions

[JSON policy document with specific actions needed]

**Notes:**
- [Important considerations, warnings, or additional context]
- [Prerequisites or dependencies]
- [Common issues or troubleshooting tips]
```

## Detailed Example

**User Request:**
```
Create an EC2 t3.micro in us-east-1 with Amazon Linux 2,
tagged temp=true, owner=devops, auto-delete in 24h
```

**Generated Output:**

### 1. Primary Command

```bash
# First, get the latest Amazon Linux 2 AMI
python3 scripts/get_latest_ami.py --os amazon-linux-2 --region us-east-1

# Launch the instance
aws ec2 run-instances \
  --region us-east-1 \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --tag-specifications 'ResourceType=instance,Tags=[
    {Key=Name,Value=temp-instance},
    {Key=Environment,Value=dev},
    {Key=Owner,Value=devops},
    {Key=Temporary,Value=true},
    {Key=AutoDelete,Value=2026-01-06T00:00:00Z},
    {Key=CreatedBy,Value=aws-cli-automation}
  ]' \
  --output json \
  --no-cli-pager
```

### 2. Dry-Run Command

```bash
aws ec2 run-instances \
  --region us-east-1 \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --dry-run \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=temp-instance}]'
```

### 3. Cleanup Commands

```bash
# Get instance ID from tag
INSTANCE_ID=$(aws ec2 describe-instances \
  --region us-east-1 \
  --filters "Name=tag:Temporary,Values=true" "Name=instance-state-name,Values=running" \
  --query "Reservations[0].Instances[0].InstanceId" \
  --output text)

# Terminate the instance
aws ec2 terminate-instances \
  --region us-east-1 \
  --instance-ids $INSTANCE_ID \
  --output json
```

### 4. Required IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:RunInstances",
        "ec2:CreateTags",
        "ec2:DescribeInstances",
        "ec2:DescribeImages"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "ec2:TerminateInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "StringEquals": {
          "ec2:ResourceTag/Temporary": "true"
        }
      }
    }
  ]
}
```

**Notes:**
- Use `scripts/get_latest_ami.py` to find current AMI IDs (they change regularly)
- Instance will need a security group; add `--security-group-ids` if not using default
- For SSH access, add `--key-name <keypair-name>`
- AutoDelete tag enables automation with EventBridge scheduled rules
- Consider using `--instance-market-options` for spot instances to reduce costs

## Tagging Strategy

Apply comprehensive tags to all resources:

### Required Tags
- `Name`: Human-readable identifier
- `Environment`: prod/staging/dev/test
- `Owner`: Team or individual
- `CostCenter`: For billing allocation

### Temporary Resource Tags
- `Temporary`: "true" for resources that should be cleaned up
- `AutoDelete`: ISO 8601 timestamp for automated deletion
- `TTL`: Duration (e.g., "24h", "7d")

### Optional but Recommended
- `Project`: Application or project name
- `ManagedBy`: Tool managing the resource
- `CreatedBy`: User or automation
- `CreatedAt`: Creation timestamp

## Security Defaults

Always apply these security practices:

### Encryption
- Enable encryption at rest for S3, EBS, RDS
- Use AWS-managed keys (AES256) by default
- Specify KMS keys for additional control

### Network Security
- Place databases in private subnets
- Restrict security groups to minimum required ports
- Block S3 public access by default
- Use VPC endpoints for AWS service access

### IAM
- Apply least-privilege principle
- Use resource-based conditions when possible
- Document all required permissions
- Prefer IAM roles over access keys

## Cost Optimization

Include cost-saving measures:

### Right-Sizing
- Start with smaller instance types
- Use burstable (t3/t4g) for variable workloads
- Suggest spot instances for fault-tolerant workloads

### Lifecycle Management
- Add S3 lifecycle policies for data retention
- Enable automated backup retention limits
- Suggest auto-scaling for dynamic workloads

### Monitoring
- Recommend billing alerts
- Suggest cost allocation tags
- Note expensive resources (NAT gateways, data transfer)

## Helper Scripts

### Get Latest AMI

Use `scripts/get_latest_ami.py` to find current AMI IDs:

```bash
# Amazon Linux 2
python3 scripts/get_latest_ami.py --os amazon-linux-2 --region us-east-1

# Ubuntu 22.04
python3 scripts/get_latest_ami.py --os ubuntu-22.04 --region us-west-2

# View as JSON
python3 scripts/get_latest_ami.py --os amazon-linux-2 --region us-east-1 --json
```

**Supported operating systems:**
- amazon-linux-2, amazon-linux-2023
- ubuntu-20.04, ubuntu-22.04, ubuntu-24.04
- debian-11, debian-12
- rhel-8, rhel-9

## Common Patterns

### Multi-Step Operations

When requests require multiple commands, provide them in order with explanations:

```bash
# Step 1: Create VPC
aws ec2 create-vpc ...

# Step 2: Create subnet
aws ec2 create-subnet ...

# Step 3: Create security group
aws ec2 create-security-group ...

# Step 4: Launch instance
aws ec2 run-instances ...
```

### Conditional Logic

For requests with alternatives, present options:

```markdown
**Option A: Use default VPC** (simpler, less secure)
[command]

**Option B: Create custom VPC** (recommended for production)
[commands]
```

### Environment-Specific Commands

Adjust parameters based on environment:

```bash
# Development
--instance-type t3.micro \
--multi-az false \
--backup-retention-period 1

# Production
--instance-type m5.large \
--multi-az true \
--backup-retention-period 30
```

## Troubleshooting

Include common issues and solutions:

### AMI Not Found
- AMI IDs are region-specific
- Use `scripts/get_latest_ami.py` to find current IDs
- Check AWS Systems Manager Parameter Store for official AMIs

### Insufficient Permissions
- Run dry-run command to validate permissions
- Review IAM policy in output
- Check for service-linked role requirements

### Resource Limits
- Check service quotas: `aws service-quotas list-service-quotas --service-code <service>`
- Request limit increases through AWS Support
- Consider alternative instance types or regions

### VPC/Networking Requirements
- Many services require VPC configuration
- Specify `--subnet-id` and `--security-group-ids`
- Use default VPC for simple tests, custom VPC for production

## Service Coverage

This skill covers commonly-used AWS services. For detailed patterns:

- **EC2**: Instance launch, spot instances, user data → [references/ec2.md](references/ec2.md)
- **S3**: Bucket creation, encryption, versioning, lifecycle → [references/s3.md](references/s3.md)
- **Lambda**: Function deployment, configuration, VPC, triggers → [references/lambda.md](references/lambda.md)
- **RDS**: Database instances, snapshots, multi-AZ, replicas → [references/rds.md](references/rds.md)
- **Best Practices**: Tagging, security, cost optimization → [references/best-practices.md](references/best-practices.md)

For services not covered in references, apply the same structured approach: primary command, dry-run, cleanup, IAM permissions, and best practices.
