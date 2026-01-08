# Sample Terraform configuration with intentional issues for testing

provider "aws" {
  region = "us-east-1"
}

# ISSUE: S3 bucket without encryption
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake-prod"
}

# ISSUE: Publicly accessible RDS instance
resource "aws_db_instance" "mysql" {
  identifier           = "production-db"
  engine              = "mysql"
  engine_version      = "5.7"
  instance_class      = "db.m5.2xlarge"  # ISSUE: Oversized for small app
  allocated_storage   = 100
  publicly_accessible = true  # ISSUE: Security risk
  multi_az            = false # ISSUE: Single AZ

  username = "admin"
  password = "hardcoded-password-123"  # ISSUE: Hardcoded password

  backup_retention_period = 0  # ISSUE: No backups
  skip_final_snapshot    = true
}

# ISSUE: Security group allows all traffic
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Web server security group"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # ISSUE: Open to world
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ISSUE: EC2 without auto-scaling, single AZ
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.large"  # ISSUE: Could use t3 for better price/performance

  vpc_security_group_ids = [aws_security_group.web.id]

  root_block_device {
    volume_type = "gp2"  # ISSUE: gp3 is more cost-effective
    volume_size = 100
    encrypted   = false  # ISSUE: Unencrypted root volume
  }

  # ISSUE: No tags for cost allocation
}

# ISSUE: IAM role with wildcard permissions
resource "aws_iam_role" "app_role" {
  name = "app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "app_policy" {
  name = "app-policy"
  role = aws_iam_role.app_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action   = "*"  # ISSUE: Wildcard permissions
      Effect   = "Allow"
      Resource = "*"  # ISSUE: All resources
    }]
  })
}

# ISSUE: Single NAT Gateway (not HA)
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = "subnet-12345678"  # ISSUE: Hardcoded ID
}

resource "aws_eip" "nat" {
  domain = "vpc"
}

# ISSUE: CloudWatch Logs without retention
resource "aws_cloudwatch_log_group" "app_logs" {
  name = "/aws/application/logs"
  # Missing retention_in_days - logs kept forever (cost issue)
}
