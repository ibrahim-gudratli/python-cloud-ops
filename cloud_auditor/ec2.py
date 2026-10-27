def audit_instances(ec2_client):
    findings = []

    paginator = ec2_client.get_paginator("describe_instances")

    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]

                tags = {
                    tag["Key"]: tag["Value"]
                    for tag in instance.get("Tags", [])
                }

                if "Environment" not in tags:
                    findings.append({
                        "severity": "LOW",
                        "resource": instance_id,
                        "issue": "Missing Environment tag"
                    })

    return findings