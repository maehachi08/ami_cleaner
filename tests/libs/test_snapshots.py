import sys
import argparse

import unittest
from unittest.mock import patch

from ami_cleaner.libs import snapshots as target


class TestSnapshot(unittest.TestCase):

    image = {
        'ImageId': 'ami-0123456789abc',
        'Name': 'ami-name-0123456789abc',
        'CreationDate': '2019-10-01T14:16:22.000Z',
        'BlockDeviceMappings': [
            {
                'DeviceName': '/dev/sda',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'SnapshotId': 'snap-0123456789'
                }
            }
        ]
    }

    image_without_SnapshotId = {
        'ImageId': 'ami-0123456789abc',
        'Name': 'ami-name-0123456789abc',
        'CreationDate': '2019-10-01T14:16:22.000Z',
        'BlockDeviceMappings': [
            {
                'DeviceName': '/dev/sda',
                'Ebs': {
                    'DeleteOnTermination': True
                }
            }
        ]
    }

    def _create_parser(self, option, value):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(option, default=value)
        args = arg_parser.parse_args()
        return args

    @patch('ami_cleaner.libs.snapshots._delete_specified_snapshot')
    def test_delete_image_snapshopt_with_SnapshotId(self, mocked_delete_snapshot):
        args = self._create_parser('--region', 'ap-northeast-1')
        target.delete_image_snapshopt(args, self.image)
        self.assertEqual(mocked_delete_snapshot.call_count, 1)

    @patch('ami_cleaner.libs.snapshots._delete_specified_snapshot')
    def test_delete_image_snapshopt_without_SnapshotId(self, mocked_delete_snapshot):
        args = self._create_parser('--region', 'ap-northeast-1')
        target.delete_image_snapshopt(args, self.image_without_SnapshotId)
        self.assertEqual(mocked_delete_snapshot.call_count, 0)

    @patch('ami_cleaner.libs.snapshots._get_client')
    def test_delete_specified_snapshot(self, mocked_client):
        args = self._create_parser('--region', 'ap-northeast-1')
        snapshot_id = self.image['BlockDeviceMappings'][0]['Ebs']['SnapshotId']
        target._delete_specified_snapshot(args, snapshot_id)

    @patch('ami_cleaner.libs.snapshots.boto3')
    def test_get_client(self, mocked_boto3):
        args = self._create_parser('--region', 'ap-northeast-1')
        target._get_client(args.region)
