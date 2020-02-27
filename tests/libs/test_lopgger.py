import sys
import argparse
import logging

import unittest

from ami_cleaner.libs import logger as target


class TestLogger(unittest.TestCase):

    def test_get_logger(self):
        # prepare
        sys.argv = ['']
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('--debug', action='store_true')
        args = arg_parser.parse_args()

        # run test
        response = target.get_logger(args)

        # assert
        self.assertTrue(isinstance(response, logging.Logger))
