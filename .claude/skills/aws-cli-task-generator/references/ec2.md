# EC2 Command Patterns

## Basic Instance Launch

```bash
aws ec2 run-instances \
  --region <region> \
  --image-id <ami-id> \
  --instance-type <type> \
  --key-name <key-pair-name> \
  --security-group-ids <sg-id> \
  --subnet-id <subnet-id> \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=<name>}]' \
  --output json
```

## Common Instance Types by Use Case

- **General Purpose**: t3.micro, t3.small, t3.medium, m5.large
- **Compute Optimized**: c5.large, c5.xlarge, c6i.large
- **Memory Optimized**: r5.large, r5.xlarge, r6i.large
- **Storage Optimized**: i3.large, d2.xlarge
- **GPU**: p3.2xlarge, g4dn.xlarge

## Spot Instances

```bash
aws ec2 run-instances \
  --region us-east-1 \
  --image-id ami-xxxxx \
  --instance-type t3.micro \
  --instance-market-options 'MarketType=spot,SpotOptions={MaxPrice=0.05,SpotInstanceType=one-time}'
```

## User Data Script

```bash
aws ec2 run-instances \
  --user-data file://script.sh \
  ...
```

## Cleanup Commands

```bash
# Terminate instance
aws ec2 terminate-instances --instance-ids <instance-id>

# Delete security group (after instance terminated)
aws ec2 delete-security-group --group-id <sg-id>

# Release elastic IP
aws ec2 release-address --allocation-id <eip-alloc-id>
```

## IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:RunInstances",
        "ec2:TerminateInstances",
        "ec2:CreateTags",
        "ec2:DescribeInstances",
        "ec2:DescribeImages",
        "ec2:DescribeKeyPairs",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeSubnets"
      ],
      "Resource": "*"
    }
  ]
}
```
