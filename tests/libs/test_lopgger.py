import sys
import argparse
import logging

import unittest

from ami_cleaner.libs import logger as target


class TestLogger(unittest.TestCase):

    def test_get_logger(self):
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--debug', action='store_true')
        args = arg_parser.parse_args()
        response = target.get_logger(args)
        self.assertTrue(isinstance(response, logging.Logger))
