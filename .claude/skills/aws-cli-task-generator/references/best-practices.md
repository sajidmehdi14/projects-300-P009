# AWS CLI Best Practices

## Tagging Standards

### Required Tags (Minimum)
- `Name`: Human-readable resource name
- `Environment`: prod/staging/dev/test
- `Owner`: Team or individual responsible
- `CostCenter`: For billing allocation

### Recommended Tags
- `Project`: Project or application name
- `ManagedBy`: Tool managing the resource (terraform/cloudformation/manual)
- `CreatedBy`: User or automation that created it
- `CreatedAt`: Timestamp (ISO 8601 format)

### Temporary Resource Tags
- `Temporary`: true/false
- `AutoDelete`: Timestamp when resource should be deleted
- `TTL`: Time-to-live in hours/days

### Example Tag Set
```json
[
  {Key=Name,Value=web-server-prod-01},
  {Key=Environment,Value=prod},
  {Key=Owner,Value=platform-team},
  {Key=CostCenter,Value=engineering},
  {Key=Project,Value=customer-portal},
  {Key=ManagedBy,Value=terraform},
  {Key=Temporary,Value=false}
]
```

## Command Structure Best Practices

### Always Specify Region
```bash
# Good
aws ec2 describe-instances --region us-east-1

# Bad (relies on default/config)
aws ec2 describe-instances
```

### Use Explicit Output Format
```bash
# Good - machine parseable
aws ec2 describe-instances --output json

# Good - human readable
aws ec2 describe-instances --output table

# Avoid default (may change)
aws ec2 describe-instances
```

### Disable Pager for Scripts
```bash
# Good for scripts/automation
aws ec2 describe-instances --no-cli-pager --output json

# Good for interactive use
aws ec2 describe-instances --output table
```

### Use Query to Filter Results
```bash
# Get only running instance IDs
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[*].Instances[*].InstanceId" \
  --output text
```

### Use Profiles for Multiple Accounts
```bash
# Good - explicit profile
aws s3 ls --profile production

# Use in commands
aws ec2 describe-instances --region us-east-1 --profile dev
```

## Security Best Practices

### Encryption at Rest
Always enable encryption for:
- S3 buckets
- EBS volumes
- RDS databases
- DynamoDB tables

### Network Security
- Use private subnets for databases and backend services
- Restrict security groups to minimum required ports
- Use VPC endpoints for AWS service access
- Block public access on S3 buckets by default

### IAM Best Practices
- Use least-privilege permissions
- Prefer IAM roles over access keys
- Enable MFA for sensitive operations
- Rotate credentials regularly
- Use resource-based policies when possible

## Cost Optimization

### Right-Sizing
- Start small, scale up as needed
- Use burstable instances (t3/t4g) for variable workloads
- Use spot instances for non-critical workloads

### Lifecycle Management
- Set S3 lifecycle policies for data retention
- Enable automated snapshots with retention policies
- Use auto-scaling for dynamic workloads

### Monitoring
- Set up billing alerts
- Use Cost Explorer for analysis
- Tag all resources for cost allocation
- Enable AWS Cost Anomaly Detection

## Dry-Run Support

Many AWS services support `--dry-run` to validate permissions and parameters:

```bash
# EC2
aws ec2 run-instances --dry-run ...

# S3 (limited)
aws s3api put-object --dry-run ...
```

Not all services support dry-run. When unavailable, validate with describe/list commands first.

## Error Handling

### Check AWS CLI Version
```bash
aws --version
```

### Verify Credentials
```bash
aws sts get-caller-identity
```

### Test Region Availability
```bash
aws ec2 describe-regions --output table
```

### Check Service Quotas
```bash
aws service-quotas list-service-quotas \
  --service-code ec2 \
  --query "Quotas[?QuotaName=='Running On-Demand Standard instances']"
```

## Output Handling

### Save to File
```bash
aws ec2 describe-instances > instances.json
```

### Pretty Print JSON
```bash
aws ec2 describe-instances | jq '.'
```

### Extract Specific Fields
```bash
# Get all instance IDs
aws ec2 describe-instances \
  --query "Reservations[*].Instances[*].InstanceId" \
  --output text

# Get instance ID and state
aws ec2 describe-instances \
  --query "Reservations[*].Instances[*].[InstanceId,State.Name]" \
  --output table
```

## Naming Conventions

### Resource Names
- Use lowercase with hyphens: `web-server-prod-01`
- Include environment: `myapp-prod-db`, `myapp-dev-db`
- Include region for multi-region: `myapp-us-east-1-prod`
- Use sequential numbers: `-01`, `-02`, `-03`

### Bucket Names
- Must be globally unique
- Use DNS-compatible naming
- Include organization prefix: `myorg-backups-prod`
- Consider region: `myorg-logs-us-west-2`
