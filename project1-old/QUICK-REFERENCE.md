# Terraform Production Reviewer - Quick Reference

## One-Liner Usage

```bash
terraform review <path>
```

## What It Checks

### Security (CRITICAL/HIGH Priority)
- [ ] Unencrypted S3 buckets, EBS volumes, RDS
- [ ] Public exposure (0.0.0.0/0 security groups)
- [ ] Hardcoded passwords/secrets
- [ ] Wildcard IAM permissions (*, Resource=*)
- [ ] Missing CloudTrail, VPC Flow Logs
- [ ] Publicly accessible databases

### Cost (HIGH/MEDIUM Priority)
- [ ] Oversized instances (right-sizing)
- [ ] GP2 volumes (should be GP3)
- [ ] Multi-AZ on non-prod
- [ ] Unnecessary NAT Gateways
- [ ] Missing auto-scaling
- [ ] No S3 lifecycle policies
- [ ] Missing CloudWatch log retention

### Availability (HIGH/MEDIUM Priority)
- [ ] Single AZ deployments
- [ ] No auto-scaling groups
- [ ] Missing backup retention
- [ ] Single NAT Gateway
- [ ] No health checks
- [ ] Hard-coded dependencies

### Well-Architected
Maps all findings to 6 pillars:
1. Operational Excellence
2. Security
3. Reliability
4. Performance Efficiency
5. Cost Optimization
6. Sustainability

## Output Format

```
# Terraform Production Review Report
**Directory**: ./infrastructure
**Files Analyzed**: 12

## EXECUTIVE SUMMARY
Risk Overview:
- CRITICAL: 2
- HIGH: 5
- MEDIUM: 8
- LOW: 3

## 1. SECURITY FINDINGS
[Detailed findings with code fixes]

## 2. COST OPTIMIZATION FINDINGS
[Savings opportunities with estimates]

## 3. AVAILABILITY & RELIABILITY FINDINGS
[HA improvements]

## 4. AWS WELL-ARCHITECTED VIOLATIONS
[Pillar-specific issues]

## CI/CD INTEGRATION
```json
{
  "summary": {...},
  "findings": [...]
}
```
```

## Severity Guide

| Level | Action | Examples |
|-------|--------|----------|
| **CRITICAL** | Fix immediately | Hardcoded password, public RDS, no encryption |
| **HIGH** | Fix this sprint | Wildcard IAM, 0.0.0.0/0 SG, major cost waste |
| **MEDIUM** | Fix this month | Single AZ, right-sizing, GP2 volumes |
| **LOW** | Backlog | Missing tags, log retention, minor optimizations |

## Common Findings & Fixes

### 1. Unencrypted S3 Bucket
```hcl
# Add encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "bucket" {
  bucket = aws_s3_bucket.bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}
```

### 2. Open Security Group
```hcl
# Change from
cidr_blocks = ["0.0.0.0/0"]

# To specific CIDR
cidr_blocks = ["10.0.0.0/8"]
```

### 3. Hardcoded Password
```hcl
# Change from
password = "hardcoded123"

# To secret
password = data.aws_secretsmanager_secret_version.db_password.secret_string
```

### 4. Single AZ RDS
```hcl
# Add
multi_az = true
```

### 5. GP2 to GP3
```hcl
# Change from
volume_type = "gp2"

# To
volume_type = "gp3"
```

### 6. Wildcard IAM
```hcl
# Change from
Action   = "*"
Resource = "*"

# To specific
Action   = ["s3:GetObject", "s3:PutObject"]
Resource = ["arn:aws:s3:::my-bucket/*"]
```

## CI/CD Integration Examples

### Fail on Critical
```bash
CRITICAL=$(grep -c "CRITICAL" review.md || true)
[ "$CRITICAL" -gt 0 ] && exit 1
```

### Parse JSON
```python
import json
data = json.loads(json_block)
if data['summary']['severity_breakdown']['critical'] > 0:
    raise Exception("Critical findings!")
```

### GitHub Action
```yaml
- run: claude terraform-production-reviewer ./terraform > review.md
- run: |
    if grep -q "CRITICAL" review.md; then
      exit 1
    fi
```

## Installation

```bash
# Copy skill
cp terraform-production-reviewer.skill ~/.claude/skills/

# Start Claude Code
claude

# Run review
terraform review ./your-infra
```

## Pro Tips

1. **Run before every production apply**
   ```bash
   terraform review . && terraform apply
   ```

2. **Track cost savings**
   ```bash
   grep "Savings:" review.md | awk '{sum+=$2} END {print "$"sum"/mo"}'
   ```

3. **Export findings list**
   ```bash
   grep "^###" review.md > findings.txt
   ```

4. **Module-by-module review**
   ```bash
   for dir in modules/*; do
     terraform review $dir
   done
   ```

5. **Compare before/after**
   ```bash
   terraform review . > before.md
   # Make fixes
   terraform review . > after.md
   diff before.md after.md
   ```

## Test with Sample

```bash
# Review the included sample with intentional issues
terraform review ./sample-terraform

# Expected: 15+ findings across all severity levels
```

## File Coverage

Analyzes:
- `*.tf` - All Terraform files
- `*.tfvars` - Variable definitions

Ignores:
- `.terraform/` directory
- State files (`.tfstate`)
- Lock files

## Support

- Full docs: [SKILL-USAGE.md](./SKILL-USAGE.md)
- Sample code: [sample-terraform/](./sample-terraform/)
- Issues: File on GitHub

---

**Remember**: Every finding includes exact resource names and concrete fixes. No generic advice!
