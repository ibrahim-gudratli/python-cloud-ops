# AWS Infrastructure Auditor

A Python-based CLI tool that audits AWS infrastructure across multiple regions to identify potential security risks, configuration issues, and unused resources.

Built with Python and Boto3, the tool performs read-only infrastructure checks and generates structured JSON reports.

## Features

- **Multi-region auditing** — Automatically discovers and scans enabled AWS regions.
- **EC2 auditing** — Identifies instances missing the `Environment` tag.
- **EBS auditing** — Detects unattached and unencrypted EBS volumes.
- **Security group auditing** — Detects inbound rules exposing SSH (port 22) to `0.0.0.0/0`.
- **JSON reporting** — Exports findings with timestamps, resource identifiers, regions, and severity levels.
- **Automated testing** — Uses pytest and mocked AWS responses.
- **Continuous Integration** — Runs automated tests through GitHub Actions.

## Architecture

```text
AWS Infrastructure Auditor
│
├── CLI (__main__.py)
│   ├── AWS Region Discovery
│   │
│   ├── EC2 Auditor
│   ├── EBS Auditor
│   └── Security Group Auditor
│
├── JSON Report Generator
│
└── Automated Tests (pytest)
```

## Technology Stack

- Python 3
- AWS Boto3 SDK
- AWS EC2 APIs
- pytest
- GitHub Actions
- JSON

## Installation

Clone the repository:

```bash
git clone https://github.com/ibrahim-gudratli/python-cloud-ops.git
cd python-cloud-ops
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## AWS Authentication

The application uses Boto3's default credential provider chain.

Configure AWS credentials using an appropriate authentication method, such as an AWS CLI profile or IAM Identity Center.

Verify authentication:

```bash
aws sts get-caller-identity
```

The AWS identity must have permission to describe EC2 instances, EBS volumes, security groups, and AWS regions.

The tool performs read-only operations and does not modify AWS resources.

## Usage

### Audit all enabled AWS regions

```bash
python -m cloud_auditor
```

### Audit a specific region

```bash
python -m cloud_auditor --region eu-north-1
```

### Example Output

```text
Auditing region: eu-north-1

[LOW] i-0123456789abcdef0: Missing Environment tag
[MEDIUM] vol-0123456789abcdef0: Unencrypted EBS volume
[HIGH] sg-0123456789abcdef0: SSH exposed to the internet

Total findings: 3

Report saved to audit-report.json
```

### JSON Report

The application generates an `audit-report.json` file.

Example:

```json
{
    "timestamp": "2026-10-27T01:10:05+00:00",
    "region": "eu-north-1",
    "total_findings": 1,
    "findings": [
        {
            "severity": "MEDIUM",
            "resource": "vol-0123456789abcdef0",
            "issue": "Unencrypted EBS volume",
            "region": "eu-north-1"
        }
    ]
}
```

## Automated Testing

Run all tests:

```bash
python -m pytest tests/ -v
```

Tests use mocked AWS API responses, so they do not require AWS credentials or access to live infrastructure.

## CI/CD

GitHub Actions automatically executes the test suite when code is pushed or a pull request is opened.

The CI pipeline:

1. Checks out the repository.
2. Configures Python.
3. Installs dependencies.
4. Runs pytest.

No AWS credentials are required for CI.

## Project Structure

```text
python-cloud-ops/
├── .github/
│   └── workflows/
│       └── ci.yml
├── cloud_auditor/
│   ├── __init__.py
│   ├── __main__.py
│   ├── ec2.py
│   ├── ebs.py
│   ├── security.py
│   └── report.py
├── tests/
│   ├── test_ec2.py
│   ├── test_ebs.py
│   └── test_security.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Current Limitations

- AWS API failures are not yet handled individually per region.
- Security group auditing currently checks unrestricted IPv4 SSH access only.
- Cost estimates are not calculated.
- Reports are saved locally.
- The test suite covers selected scenarios rather than all edge cases.

## Future Improvements

- Additional AWS security and configuration checks.
- Cost optimization recommendations