import sys
import argparse

import unittest
from unittest.mock import patch

from ami_cleaner import ami_cleaner as target


class TestImages(unittest.TestCase):

    images = {
        'Images': [
            {
                'ImageId': 'ami-0123456789abc',
                'Name': 'ami-name-0123456789abc',
                'CreationDate': '2019-10-01T14:16:22.000Z'
            }
        ]
    }

    def _create_parser(self, option, value):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()

        if option == '--dry-run' and not value:
            arg_parser.add_argument(option, action='store_true')

        elif option == '--dry-run' and value:
            arg_parser.add_argument(option, default=value)

        else:
            arg_parser.add_argument(option, default=value)

        return arg_parser

    @patch('ami_cleaner.ami_cleaner.print_tableview')
    @patch('ami_cleaner.ami_cleaner.get_images_should_deregister')
    @patch('ami_cleaner.ami_cleaner.get_logger')
    @patch('ami_cleaner.ami_cleaner.tag_filters_chain')
    @patch('ami_cleaner.ami_cleaner.create_parser')
    def test_main_with_dry_run(self,
                               mocked_create_parser,
                               mocked_tag_filters_chain,
                               mocked_logger,
                               mocked_get_images,
                               mocked_print_tableview):
        args = self._create_parser('--dry-run', True)
        mocked_create_parser.return_value = args
        mocked_get_images.return_value = self.images
        target.main()
        self.assertEqual(mocked_print_tableview.call_count, 1)

    @patch('ami_cleaner.ami_cleaner.print_tableview')
    @patch('ami_cleaner.ami_cleaner.get_images_should_deregister')
    @patch('ami_cleaner.ami_cleaner.get_logger')
    @patch('ami_cleaner.ami_cleaner.tag_filters_chain')
    @patch('ami_cleaner.ami_cleaner.create_parser')
    def test_main_with_dry_run_without_images(self,
                                              mocked_create_parser,
                                              mocked_tag_filters_chain,
                                              mocked_logger,
                                              mocked_get_images,
                                              mocked_print_tableview):
        args = self._create_parser('--dry-run', True)
        mocked_create_parser.return_value = args
        mocked_get_images.return_value = {'Images': []}
        target.main()
        self.assertEqual(mocked_print_tableview.call_count, 0)

    @patch('ami_cleaner.ami_cleaner.delete_image_snapshopt')
    @patch('ami_cleaner.ami_cleaner.deregister_image')
    @patch('ami_cleaner.ami_cleaner.print_tableview')
    @patch('ami_cleaner.ami_cleaner.get_images_should_deregister')
    @patch('ami_cleaner.ami_cleaner.get_logger')
    @patch('ami_cleaner.ami_cleaner.tag_filters_chain')
    @patch('ami_cleaner.ami_cleaner.create_parser')
    def test_main_without_images(self,
                                 mocked_create_parser,
                                 mocked_tag_filters_chain,
                                 mocked_logger,
                                 mocked_get_images,
                                 mocked_print_tableview,
                                 mocked_deregister_image,
                                 mocked_delete_image_snapshopt):

        arg_parser = self._create_parser('--dry-run', None)
        args = arg_parser.parse_args()
        mocked_tag_filters_chain.return_value = args
        mocked_get_images.return_value = {'Images': []}

        target.main()
        self.assertEqual(mocked_print_tableview.call_count, 0)
        self.assertEqual(mocked_deregister_image.call_count, 0)
        self.assertEqual(mocked_delete_image_snapshopt.call_count, 0)

    @patch('ami_cleaner.ami_cleaner.delete_image_snapshopt')
    @patch('ami_cleaner.ami_cleaner.deregister_image')
    @patch('ami_cleaner.ami_cleaner.print_tableview')
    @patch('ami_cleaner.ami_cleaner.get_images_should_deregister')
    @patch('ami_cleaner.ami_cleaner.get_logger')
    @patch('ami_cleaner.ami_cleaner.tag_filters_chain')
    @patch('ami_cleaner.ami_cleaner.create_parser')
    def test_main_with_images(self,
                              mocked_create_parser,
                              mocked_tag_filters_chain,
                              mocked_logger,
                              mocked_get_images,
                              mocked_print_tableview,
                              mocked_deregister_image,
                              mocked_delete_image_snapshopt):

        arg_parser = self._create_parser('--dry-run', None)
        args = arg_parser.parse_args()
        mocked_tag_filters_chain.return_value = args
        mocked_get_images.return_value = self.images

        target.main()
        self.assertEqual(mocked_print_tableview.call_count, 0)
        self.assertEqual(mocked_deregister_image.call_count, 1)
        self.assertEqual(mocked_delete_image_snapshopt.call_count, 1)

    @patch('ami_cleaner.ami_cleaner.delete_image_snapshopt')
    @patch('ami_cleaner.ami_cleaner.deregister_image')
    @patch('ami_cleaner.ami_cleaner.print_tableview')
    @patch('ami_cleaner.ami_cleaner.get_images_should_deregister')
    @patch('ami_cleaner.ami_cleaner.get_logger')
    @patch('ami_cleaner.ami_cleaner.tag_filters_chain')
    @patch('ami_cleaner.ami_cleaner.create_parser')
    def test_main_with_exception(self,
                                 mocked_create_parser,
                                 mocked_tag_filters_chain,
                                 mocked_logger,
                                 mocked_get_images,
                                 mocked_print_tableview,
                                 mocked_deregister_image,
                                 mocked_delete_image_snapshopt):

        arg_parser = self._create_parser('--dry-run', None)
        args = arg_parser.parse_args()
        mocked_tag_filters_chain.return_value = args
        mocked_get_images.side_effect = Exception('test exception')

        target.main()
        self.assertEqual(mocked_print_tableview.call_count, 0)
        self.assertEqual(mocked_deregister_image.call_count, 0)
        self.assertEqual(mocked_delete_image_snapshopt.call_count, 0)
