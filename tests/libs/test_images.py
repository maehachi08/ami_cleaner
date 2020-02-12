import sys
import argparse

import unittest
from unittest.mock import patch

from ami_cleaner.libs import images as target


class TestImages(unittest.TestCase):

    def test_print_tableview(self):
        images = {
            'Images': [
                {
                    'ImageId': 'ami-0123456789abc',
                    'Name': 'ami-name-0123456789abc',
                    'CreationDate': '2020-02-10T12:12:12.123456'
                }
            ]
        }
        target.print_tableview(images)

    @patch('ami_cleaner.libs.images._get_images_should_deregister')
    @patch('ami_cleaner.libs.images._get_client')
    def test_get_images_should_deregister(self,
                                          mocked_client,
                                          mocked_get_images_should_deregister):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--region', default='ap-northeast-1')
        args = arg_parser.parse_args()
        target.get_images_should_deregister(args)

    @patch('ami_cleaner.libs.images._get_client')
    def test_deregister_image(self, mocked_client):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--region', default='ap-northeast-1')
        args = arg_parser.parse_args()
        image_id = 'ami-0123456789abc'
        target.deregister_image(args, image_id)

    @patch('ami_cleaner.libs.images.boto3')
    def test_get_client(self, mocked_boto3):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--region', default='ap-northeast-1')
        args = arg_parser.parse_args()
        target._get_client(args.region)

    @patch('ami_cleaner.libs.images._get_inatances_specific_image_id')
    @patch('ami_cleaner.libs.images._get_client')
    def test_is_using_image_true(self, mocked_client, mocked_get_inatances):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--region', default='ap-northeast-1')
        args = arg_parser.parse_args()
        image = {
            'ImageId': 'ami-0123456789abc',
            'Name': 'ami-name-0123456789abc',
            'CreationDate': '2020-02-10T12:12:12.123456'
        }

        mocked_get_inatances.return_value = {'Reservations': [{'Instances': ''}]}
        response = target._is_using_image(args, image)
        self.assertEqual(response, True)

    @patch('ami_cleaner.libs.images._get_inatances_specific_image_id')
    @patch('ami_cleaner.libs.images._get_client')
    def test_is_using_image_false(self, mocked_client, mocked_get_inatances):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--region', default='ap-northeast-1')
        args = arg_parser.parse_args()
        image = {
            'ImageId': 'ami-0123456789abc',
            'Name': 'ami-name-0123456789abc',
            'CreationDate': '2020-02-10T12:12:12.123456'
        }

        mocked_get_inatances.return_value = {'Reservations': []}
        response = target._is_using_image(args, image)
        self.assertEqual(response, False)

