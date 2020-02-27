import unittest
from unittest.mock import patch

from ami_cleaner.libs import sts as target


class TestSts(unittest.TestCase):

    @patch('ami_cleaner.libs.sts.boto3.client')
    def test_get_account_id(self, mocked_client):
        # prepare
        mocked_client('sts').get_caller_identity.return_value = {'Account': '0123456789'}

        # run test
        response = target.get_account_id()

        # assert
        self.assertEqual(response, '0123456789')
