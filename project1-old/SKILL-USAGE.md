# Terraform Production Reviewer Skill

## Overview

A comprehensive Claude Code skill that analyzes Terraform configurations for production readiness, covering security, cost, availability, and AWS Well-Architected Framework compliance.

## Features

- **Security Analysis**: Encryption, IAM policies, network exposure, secrets management, logging
- **Cost Optimization**: Right-sizing, storage optimization, networking costs, waste reduction
- **Availability Review**: Multi-AZ deployments, redundancy, backups, auto-scaling
- **Well-Architected Compliance**: Maps findings to all 6 AWS pillars
- **Severity Classification**: CRITICAL, HIGH, MEDIUM, LOW
- **Concrete Fixes**: Every finding includes exact code snippets
- **CI/CD Integration**: JSON output for automated pipelines

## Installation

1. Copy `terraform-production-reviewer.skill` to your Claude Code skills directory
2. Reload Claude Code or restart your session

## Usage

### Basic Invocation

```bash
terraform review ./infrastructure/prod
```

### Alternative Commands

```bash
terraform-production-reviewer ./terraform
tf review ./modules/vpc
infrastructure review /path/to/terraform
```

### Expected Output

The skill generates a structured report with:

1. **Executive Summary** - Quick overview of findings
2. **Security Findings** - Detailed security vulnerabilities with fixes
3. **Cost Optimization** - Cost savings opportunities with dollar estimates
4. **Availability Findings** - Reliability and redundancy improvements
5. **Well-Architected Violations** - Framework compliance gaps
6. **Summary & Recommendations** - Prioritized action items
7. **JSON Summary Block** - Machine-parseable output for CI/CD

## Example Findings

### Security Finding Example
```
### CRITICAL - S3 Bucket Without Encryption
**Resource**: `aws_s3_bucket.data_lake`
**File**: `storage.tf:15`

**Issue**:
S3 bucket lacks server-side encryption, exposing data at rest.

**Risk**:
Potential data breach, compliance violations (GDPR, HIPAA).

**Remediation**:
```hcl
# Current configuration
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake"
}

# Recommended fix
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
  }
}
```
```

### Cost Finding Example
```
### HIGH - Oversized RDS Instance
**Resource**: `aws_db_instance.mysql`
**File**: `database.tf:42`

**Issue**:
Database using db.m5.2xlarge for low-traffic application.

**Cost Impact**:
Estimated: $560/month

**Remediation**:
```hcl
# Current configuration
instance_class = "db.m5.2xlarge"

# Cost-optimized configuration
instance_class = "db.t4g.large"
```

**Savings**: ~$420/month
```

## CI/CD Integration

The JSON summary block can be parsed by CI/CD pipelines:

```bash
# Example: Fail build if CRITICAL findings exist
claude-code terraform-production-reviewer ./terraform | \
  jq -e '.summary.severity_breakdown.critical == 0'
```

```python
# Example: Python integration
import json
import subprocess

result = subprocess.run(
    ['claude-code', 'terraform-production-reviewer', './terraform'],
    capture_output=True,
    text=True
)

# Extract JSON block
report = result.stdout
json_start = report.find('```json')
json_end = report.find('```', json_start + 7)
json_data = json.loads(report[json_start+7:json_end])

if json_data['summary']['severity_breakdown']['critical'] > 0:
    raise Exception("Critical security findings detected!")
```

## Severity Guidelines

| Severity | Description | Action Timeline |
|----------|-------------|-----------------|
| CRITICAL | Immediate security risk, data exposure, service outage | Fix immediately before deployment |
| HIGH | Significant security gap, major cost impact, single point of failure | Fix within sprint |
| MEDIUM | Security hardening, moderate cost impact, degraded resilience | Fix within 30 days |
| LOW | Best practice violation, minor optimization | Backlog for future iteration |

## What Gets Analyzed

### Included
- All `.tf` files (main, variables, outputs, modules, etc.)
- All `.tfvars` files (variable values)

### Excluded
- `.terraform/` directory
- Terraform state files (`.tfstate`)
- Lock files (`.terraform.lock.hcl`)
- Non-Terraform files

## Best Practices

1. **Run Early**: Review before `terraform apply` in production
2. **Version Control**: Track fixes in Git with clear commit messages
3. **Automate**: Integrate into CI/CD pipeline for every PR
4. **Prioritize**: Address CRITICAL/HIGH findings before deployment
5. **Document**: Record why you skip certain recommendations (if applicable)

## Limitations

- Focuses on AWS resources (Azure/GCP may have limited coverage)
- Cannot detect runtime issues (only configuration)
- Cost estimates are approximate (based on standard pricing)
- Requires actual Terraform files (cannot analyze plan files)

## Advanced Usage

### Review Specific Module
```bash
terraform review ./modules/networking
```

### Combine with Terraform Validation
```bash
terraform fmt -check && \
terraform validate && \
claude-code terraform-production-reviewer .
```

### Generate HTML Report
```bash
claude-code terraform-production-reviewer . | \
  pandoc -f markdown -t html -o report.html
```

## Troubleshooting

**Q: Skill not found**
- Ensure `.skill` file is in the correct directory
- Restart Claude Code session

**Q: Analysis takes too long**
- Break large codebases into smaller reviews
- Review module by module

**Q: False positives**
- File GitHub issue with example code
- Document exception in your architecture decision records

**Q: Missing findings**
- Ensure files have correct `.tf` extension
- Check file permissions

## Contributing

Found a bug or want to improve detection rules? Submit issues or PRs to enhance the skill.

## License

MIT License - Free to use and modify

## Version

Current: 1.0.0
Last Updated: 2026-01-08
