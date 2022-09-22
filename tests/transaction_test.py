import unittest

from mock import *
import time

from Classes.Transaction import Transaction

mock_time = Mock()
mock_time.return_value = 1234567890


class BlockTestCase(unittest.TestCase):
    @patch('time.time_ns', mock_time)
    def test_the_transaction_automatically_get_the_current_timestamp(self):
        transaction = Transaction('test_sender', 'test_recipient', 1)
        self.assertEqual(1234567890, transaction.time)

    def test_the_properties_from_the_transaction_are_correctly_set(self):
        transaction = Transaction('test_sender', 'test_recipient', 1)
        self.assertEqual('test_sender', transaction.sender)
        self.assertEqual('test_recipient', transaction.recipient)
        self.assertEqual(1, transaction.amount)
