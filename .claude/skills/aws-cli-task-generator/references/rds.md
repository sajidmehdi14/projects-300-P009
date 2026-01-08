# RDS Command Patterns

## Create Database Instance

```bash
aws rds create-db-instance \
  --db-instance-identifier <db-name> \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.4 \
  --master-username <username> \
  --master-user-password <password> \
  --allocated-storage 20 \
  --storage-type gp3 \
  --storage-encrypted \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00" \
  --preferred-maintenance-window "sun:04:00-sun:05:00" \
  --vpc-security-group-ids <sg-id> \
  --db-subnet-group-name <subnet-group-name> \
  --publicly-accessible false \
  --multi-az false \
  --tags Key=Environment,Value=dev Key=Owner,Value=devops
```

## Common Database Engines

- **PostgreSQL**: `postgres` (versions: 15.4, 14.9, 13.12)
- **MySQL**: `mysql` (versions: 8.0.35, 5.7.44)
- **MariaDB**: `mariadb` (versions: 10.11, 10.6)
- **Aurora PostgreSQL**: `aurora-postgresql`
- **Aurora MySQL**: `aurora-mysql`
- **SQL Server**: `sqlserver-ee`, `sqlserver-se`, `sqlserver-ex`, `sqlserver-web`
- **Oracle**: `oracle-ee`, `oracle-se2`

## Common Instance Classes

- **Burstable**: db.t3.micro, db.t3.small, db.t3.medium
- **General Purpose**: db.m6i.large, db.m6i.xlarge
- **Memory Optimized**: db.r6i.large, db.r6i.xlarge

## Create DB Subnet Group (Required for VPC)

```bash
aws rds create-db-subnet-group \
  --db-subnet-group-name <subnet-group-name> \
  --db-subnet-group-description "Subnet group for RDS" \
  --subnet-ids <subnet-id-1> <subnet-id-2> \
  --tags Key=Environment,Value=dev
```

## Modify Instance

```bash
aws rds modify-db-instance \
  --db-instance-identifier <db-name> \
  --db-instance-class db.t3.small \
  --allocated-storage 50 \
  --apply-immediately
```

## Create Snapshot

```bash
aws rds create-db-snapshot \
  --db-instance-identifier <db-name> \
  --db-snapshot-identifier <snapshot-name>
```

## Restore from Snapshot

```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier <new-db-name> \
  --db-snapshot-identifier <snapshot-name>
```

## Cleanup Commands

```bash
# Delete snapshot
aws rds delete-db-snapshot --db-snapshot-identifier <snapshot-name>

# Delete instance (without final snapshot - use with caution)
aws rds delete-db-instance \
  --db-instance-identifier <db-name> \
  --skip-final-snapshot

# Delete instance (with final snapshot)
aws rds delete-db-instance \
  --db-instance-identifier <db-name> \
  --final-db-snapshot-identifier <final-snapshot-name>

# Delete subnet group
aws rds delete-db-subnet-group --db-subnet-group-name <subnet-group-name>
```

## IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds:CreateDBInstance",
        "rds:DeleteDBInstance",
        "rds:ModifyDBInstance",
        "rds:CreateDBSnapshot",
        "rds:DeleteDBSnapshot",
        "rds:RestoreDBInstanceFromDBSnapshot",
        "rds:DescribeDBInstances",
        "rds:DescribeDBSnapshots",
        "rds:CreateDBSubnetGroup",
        "rds:DeleteDBSubnetGroup",
        "rds:DescribeDBSubnetGroups"
      ],
      "Resource": "*"
    }
  ]
}
```
