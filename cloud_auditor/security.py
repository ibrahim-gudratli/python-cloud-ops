def audit_security_groups(ec2_client):
    findings = []

    paginator = ec2_client.get_paginator("describe_security_groups")

    for page in paginator.paginate():
        for sg in page["SecurityGroups"]:
            for rule in sg["IpPermissions"]:
                protocol = rule.get("IpProtocol")
                from_port = rule.get("FromPort", 0)
                to_port = rule.get("ToPort", 0)

                if protocol in ("tcp", "-1") and (
                    protocol == "-1" or from_port <= 22 <= to_port
                ):
                    for ip_range in rule.get("IpRanges", []):
                        if ip_range["CidrIp"] == "0.0.0.0/0":
                            findings.append({
                                "severity": "HIGH",
                                "resource": sg["GroupId"],
                                "issue": "SSH exposed to the internet"
                            })

    return findings