import json
from datetime import datetime, timezone


def save_report(findings, region, filename="audit-report.json"):
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "region": region,
        "total_findings": len(findings),
        "findings": findings
    }

    with open(filename, "w") as file:
        json.dump(report, file, indent=4)

    print(f"\nReport saved to {filename}")
