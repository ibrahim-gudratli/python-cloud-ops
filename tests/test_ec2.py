from unittest.mock import MagicMock
from cloud_auditor.ec2 import audit_instances


def test_missing_environment_tag():
    # Simulate an AWS EC2 client
    ec2 = MagicMock()

    # Simulate AWS API response
    ec2.get_paginator.return_value.paginate.return_value = [
        {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-123456",
                            "Tags": [
                                {"Key": "Name", "Value": "web-server"}
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    findings = audit_instances(ec2)

    assert len(findings) == 1
    assert findings[0]["severity"] == "LOW"
    assert findings[0]["issue"] == "Missing Environment tag"

