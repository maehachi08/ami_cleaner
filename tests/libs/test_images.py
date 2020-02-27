import sys
import argparse
from datetime import datetime

import unittest
from unittest.mock import patch

from ami_cleaner.libs import images as target


class TestImages(unittest.TestCase):

    image = {
        'ImageId': 'ami-0123456789abc',
        'Name': 'ami-name-0123456789abc',
        'CreationDate': '2019-10-01T14:16:22.000Z'
    }

    def _create_parser(self, option, value):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(option, default=value)
        args = arg_parser.parse_args()
        return args

    def test_print_tableview(self):
        # prepare
        images = {'Images': [self.image]}

        # run test
        target.print_tableview(images)

    @patch('ami_cleaner.libs.images._get_images_should_deregister')
    @patch('ami_cleaner.libs.images._get_client')
    def test_get_images_should_deregister(self,
                                          mocked_client,
                                          mocked_get_images_should_deregister):
        # prepare
        args = self._create_parser('--region', 'ap-northeast-1')

        # run test
        target.get_images_should_deregister(args)

    @patch('ami_cleaner.libs.images._get_client')
    def test_deregister_image(self, mocked_client):
        # prepare
        args = self._create_parser('--region', 'ap-northeast-1')
        image_id = 'ami-0123456789abc'

        # run test
        target.deregister_image(args, image_id)

    @patch('ami_cleaner.libs.images.boto3')
    def test_get_client(self, mocked_boto3):
        # prepare
        args = self._create_parser('--region', 'ap-northeast-1')

        # run test
        target._get_client(args.region)

    @patch('ami_cleaner.libs.images._get_inatances_specific_image_id')
    @patch('ami_cleaner.libs.images._get_client')
    def test_is_using_image_true(self, mocked_client, mocked_get_inatances):
        # prepare
        args = self._create_parser('--region', 'ap-northeast-1')
        mocked_get_inatances.return_value = {'Reservations': [{'Instances': ''}]}

        # run test
        response = target._is_using_image(args, self.image)

        # assert
        self.assertEqual(response, True)

    @patch('ami_cleaner.libs.images._get_inatances_specific_image_id')
    @patch('ami_cleaner.libs.images._get_client')
    def test_is_using_image_false(self, mocked_client, mocked_get_inatances):
        # prepare
        args = self._create_parser('--region', 'ap-northeast-1')
        mocked_get_inatances.return_value = {'Reservations': []}

        # run test
        response = target._is_using_image(args, self.image)

        # assert
        self.assertEqual(response, False)

    @patch('ami_cleaner.libs.images._get_datetime_now')
    def test_is_creation_date_expire_limit_true(self, mocked_datetime_now):
        # prepare
        args = self._create_parser('--days', 90)
        datetime_now_str = "2020-04-01 12:00:00"
        mocked_datetime_now.return_value = datetime.strptime(datetime_now_str, '%Y-%m-%d %H:%M:%S')

        # run test
        response = target._is_creation_date_expire_limit(args, self.image)

        # assert
        self.assertEqual(response, True)

    @patch('ami_cleaner.libs.images._get_datetime_now')
    def test_is_creation_date_expire_limit_false(self, mocked_datetime_now):
        # prepare
        args = self._create_parser('--days', 90)
        datetime_now_str = "2019-12-01 12:00:00"
        mocked_datetime_now.return_value = datetime.strptime(datetime_now_str, '%Y-%m-%d %H:%M:%S')

        # run test
        response = target._is_creation_date_expire_limit(args, self.image)

        # assert
        self.assertEqual(response, False)

    def test_get_datetime_now(self):
        # run test
        response = target._get_datetime_now()

        # assert
        self.assertEqual(isinstance(response, datetime), True)

    def test__tag_filter_generate(self):
        # run test
        args = self._create_parser('--tag-filters', {'Name': 'test-image'})

        # assert
        target._tag_filter_generate(args)

    # _get_images_should_deregister test case
    #   1. no images in response of describe_images
    #   2. images expire limit and using
    #   3. images expire limit and not using
    #   4. images not expire limit and using
    #   5. images not expire limit and not using
    @patch('ami_cleaner.libs.images._tag_filter_generate')
    @patch('ami_cleaner.libs.images._get_client')
    def test_get_images_should_deregister_no_images(self,
                                                    mocked_client,
                                                    mocked_tag_filter_generate):
        # prepare
        args = self._create_parser('--owner', '0123456789')
        mocked_client.describe_images.return_value = {'Images': []}

        # run test
        respons = target._get_images_should_deregister(mocked_client, args)

        # assert
        self.assertFalse(respons['Images'])

    @patch('ami_cleaner.libs.images._is_using_image')
    @patch('ami_cleaner.libs.images._is_creation_date_expire_limit')
    @patch('ami_cleaner.libs.images._tag_filter_generate')
    @patch('ami_cleaner.libs.images._get_client')
    def test_get_images_should_deregister_is_limit_and_using(self,
                                                             mocked_client,
                                                             mocked_tag_filter_generate,
                                                             mocked_is_expire_limit,
                                                             mocked_is_using_image):
        # prepare
        args = self._create_parser('--owner', '0123456789')
        mocked_client.describe_images.return_value = {'Images': [self.image]}
        mocked_is_expire_limit.return_value = True
        mocked_is_using_image.return_value = True

        # run test
        respons = target._get_images_should_deregister(mocked_client, args)

        # assert
        self.assertFalse(respons['Images'])

    @patch('ami_cleaner.libs.images._is_using_image')
    @patch('ami_cleaner.libs.images._is_creation_date_expire_limit')
    @patch('ami_cleaner.libs.images._tag_filter_generate')
    @patch('ami_cleaner.libs.images._get_client')
    def test_get_images_should_deregister_is_limit_and_not_using(self,
                                                                 mocked_client,
                                                                 mocked_tag_filter_generate,
                                                                 mocked_is_expire_limit,
                                                                 mocked_is_using_image):
        # prepare
        args = self._create_parser('--owner', '0123456789')
        mocked_client.describe_images.return_value = {'Images': [self.image]}
        mocked_is_expire_limit.return_value = True
        mocked_is_using_image.return_value = False

        # run test
        respons = target._get_images_should_deregister(mocked_client, args)

        # assert
        self.assertTrue(respons['Images'])

    @patch('ami_cleaner.libs.images._is_using_image')
    @patch('ami_cleaner.libs.images._is_creation_date_expire_limit')
    @patch('ami_cleaner.libs.images._tag_filter_generate')
    @patch('ami_cleaner.libs.images._get_client')
    def test_get_images_should_deregister_is_not_limit_and_using(self,
                                                                 mocked_client,
                                                                 mocked_tag_filter_generate,
                                                                 mocked_is_expire_limit,
                                                                 mocked_is_using_image):
        # prepare
        args = self._create_parser('--owner', '0123456789')
        mocked_client.describe_images.return_value = {'Images': [self.image]}
        mocked_is_expire_limit.return_value = False
        mocked_is_using_image.return_value = True

        # run test
        respons = target._get_images_should_deregister(mocked_client, args)

        # assert
        self.assertFalse(respons['Images'])

    @patch('ami_cleaner.libs.images._is_using_image')
    @patch('ami_cleaner.libs.images._is_creation_date_expire_limit')
    @patch('ami_cleaner.libs.images._tag_filter_generate')
    @patch('ami_cleaner.libs.images._get_client')
    def test_get_images_should_deregister_is_not_limit_and_not_using(self,
                                                                     mocked_client,
                                                                     mocked_tag_filter_generate,
                                                                     mocked_is_expire_limit,
                                                                     mocked_is_using_image):
        # prepare
        args = self._create_parser('--owner', '0123456789')
        mocked_client.describe_images.return_value = {'Images': [self.image]}
        mocked_is_expire_limit.return_value = False
        mocked_is_using_image.return_value = False

        # run test
        respons = target._get_images_should_deregister(mocked_client, args)

        # assert
        self.assertFalse(respons['Images'])

    @patch('ami_cleaner.libs.images._get_client')
    def test_get_inatances_specific_image_id(self, mocked_client):
        # prepare
        mocked_client.describe_instances.return_value = {}

        # run test
        target._get_inatances_specific_image_id(mocked_client, self.image['ImageId'])
