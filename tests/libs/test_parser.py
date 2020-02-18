import sys
import argparse

import unittest
from unittest.mock import patch

from ami_cleaner.libs import parser as target


class TestParser(unittest.TestCase):

    def _create_parser(self, option, value):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(option, default=value)
        args = arg_parser.parse_args()
        return args

    def test_tag_filters_chain(self):
        _args = self._create_parser('--tag-filters', [{'Name': 'test-image'}, {'Env': 'development'}])
        args = target.tag_filters_chain(_args)
        self.assertDictEqual(args.tag_filters, {'Name': 'test-image', 'Env': 'development'})

    @patch('ami_cleaner.libs.parser.get_account_id')
    def test_create_parser(self, mocked_get_account_id):
        mocked_get_account_id.return_value = '0123456789'
        arg_parser = target.create_parser()
        args = arg_parser.parse_args()
        self.assertFalse(args.debug)
        self.assertFalse(args.dry_run)
        self.assertEqual(args.days, 90)
        self.assertEqual(args.region, 'ap-northeast-1')
        self.assertEqual(args.owner, '0123456789')
        self.assertListEqual(args.tag_filters, [{}])
