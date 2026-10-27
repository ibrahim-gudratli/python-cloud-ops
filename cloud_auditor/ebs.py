def audit_volumes(ec2_client):
    findings = []

    paginator = ec2_client.get_paginator("describe_volumes")

    for page in paginator.paginate():
        for volume in page["Volumes"]:
            volume_id = volume["VolumeId"]

            if volume["State"] == "available":
                findings.append({
                    "severity": "MEDIUM",
                    "resource": volume_id,
                    "issue": "Unattached EBS volume"
                })

            if not volume["Encrypted"]:
                findings.append({
                    "severity": "MEDIUM",
                    "resource": volume_id,
                    "issue": "Unencrypted EBS volume"
                })

    return findings