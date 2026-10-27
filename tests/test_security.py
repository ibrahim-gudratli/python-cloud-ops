from unittest.mock import MagicMock
from cloud_auditor.security import audit_security_groups


def test_public_ssh_access():
    ec2 = MagicMock()

    ec2.get_paginator.return_value.paginate.return_value = [
        {
            "SecurityGroups": [
                {
                    "GroupId": "sg-123456",
                    "IpPermissions": [
                        {
                            "IpProtocol": "tcp",
                            "FromPort": 22,
                            "ToPort": 22,
                            "IpRanges": [
                                {"CidrIp": "0.0.0.0/0"}
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    findings = audit_security_groups(ec2)

    assert len(findings) == 1
    assert findings[0]["severity"] == "HIGH"
    assert findings[0]["issue"] == "SSH exposed to the internet"

