import argparse
import boto3

from .ec2 import audit_instances
from .ebs import audit_volumes
from .security import audit_security_groups
from .report import save_report


def main():
    parser = argparse.ArgumentParser(
        description="Audit AWS infrastructure for potential issues"
    )

    parser.add_argument(
        "--region",
        help="Audit a specific AWS region (default: all enabled regions)"
    )

    args = parser.parse_args()

    session = boto3.Session()
    ec2 = session.client("ec2")

    if args.region:
        regions = [args.region]
    else:
        response = ec2.describe_regions(AllRegions=False)
        regions = [region["RegionName"] for region in response["Regions"]]

    all_findings = []

    for region in regions:
        print(f"\nAuditing region: {region}")

        regional_ec2 = session.client("ec2", region_name=region)

        findings = (
            audit_instances(regional_ec2)
            + audit_volumes(regional_ec2)
            + audit_security_groups(regional_ec2)
        )

        for finding in findings:
            finding["region"] = region

            print(
                f"[{finding['severity']}] "
                f"{finding['resource']}: {finding['issue']}"
            )

        all_findings.extend(findings)

    print(f"\nTotal findings: {len(all_findings)}")

    save_report(all_findings, args.region or "all")


if __name__ == "__main__":
    main()