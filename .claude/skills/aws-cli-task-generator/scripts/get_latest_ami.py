#!/usr/bin/env python3
"""
Lookup the latest AMI ID for common operating systems in a specific region.
Usage: python get_latest_ami.py --os amazon-linux-2 --region us-east-1
"""

import argparse
import json
import subprocess
import sys

# Common AMI owner IDs
AMI_OWNERS = {
    'amazon-linux-2': '137112412989',  # Amazon
    'amazon-linux-2023': '137112412989',  # Amazon
    'ubuntu-20.04': '099720109477',  # Canonical
    'ubuntu-22.04': '099720109477',  # Canonical
    'ubuntu-24.04': '099720109477',  # Canonical
    'debian-11': '136693071363',  # Debian
    'debian-12': '136693071363',  # Debian
    'rhel-8': '309956199498',  # Red Hat
    'rhel-9': '309956199498',  # Red Hat
}

# AMI name patterns
AMI_NAME_PATTERNS = {
    'amazon-linux-2': 'amzn2-ami-hvm-*-x86_64-gp2',
    'amazon-linux-2023': 'al2023-ami-*-x86_64',
    'ubuntu-20.04': 'ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*',
    'ubuntu-22.04': 'ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*',
    'ubuntu-24.04': 'ubuntu/images/hvm-ssd/ubuntu-noble-24.04-amd64-server-*',
    'debian-11': 'debian-11-amd64-*',
    'debian-12': 'debian-12-amd64-*',
    'rhel-8': 'RHEL-8*_HVM-*-x86_64-*',
    'rhel-9': 'RHEL-9*_HVM-*-x86_64-*',
}


def get_latest_ami(os_type: str, region: str) -> dict:
    """Get the latest AMI ID for a specific OS and region."""
    if os_type not in AMI_OWNERS:
        raise ValueError(f"Unsupported OS type: {os_type}. Supported: {list(AMI_OWNERS.keys())}")

    owner = AMI_OWNERS[os_type]
    name_pattern = AMI_NAME_PATTERNS[os_type]

    cmd = [
        'aws', 'ec2', 'describe-images',
        '--region', region,
        '--owners', owner,
        '--filters', f'Name=name,Values={name_pattern}',
        'Name=state,Values=available',
        '--query', 'Images | sort_by(@, &CreationDate) | [-1].[ImageId, Name, CreationDate]',
        '--output', 'json'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        if not data or not data[0]:
            raise ValueError(f"No AMI found for {os_type} in {region}")

        return {
            'ami_id': data[0][0],
            'name': data[0][1],
            'creation_date': data[0][2],
            'os_type': os_type,
            'region': region
        }
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"AWS CLI error: {e.stderr}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse AWS CLI output: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Get the latest AMI ID for common operating systems'
    )
    parser.add_argument(
        '--os',
        required=True,
        choices=list(AMI_OWNERS.keys()),
        help='Operating system type'
    )
    parser.add_argument(
        '--region',
        required=True,
        help='AWS region (e.g., us-east-1)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    args = parser.parse_args()

    try:
        ami_info = get_latest_ami(args.os, args.region)

        if args.json:
            print(json.dumps(ami_info, indent=2))
        else:
            print(f"Latest AMI for {ami_info['os_type']} in {ami_info['region']}:")
            print(f"  AMI ID: {ami_info['ami_id']}")
            print(f"  Name: {ami_info['name']}")
            print(f"  Created: {ami_info['creation_date']}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
