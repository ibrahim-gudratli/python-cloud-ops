from unittest.mock import MagicMock
from cloud_auditor.ebs import audit_volumes


def test_unattached_unencrypted_volume():
    ec2 = MagicMock()

    ec2.get_paginator.return_value.paginate.return_value = [
        {
            "Volumes": [
                {
                    "VolumeId": "vol-123456",
                    "State": "available",
                    "Encrypted": False
                }
            ]
        }
    ]

    findings = audit_volumes(ec2)

    assert len(findings) == 2
    assert findings[0]["issue"] == "Unattached EBS volume"
    assert findings[1]["issue"] == "Unencrypted EBS volume"
