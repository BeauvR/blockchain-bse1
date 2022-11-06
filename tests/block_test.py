import unittest

from Classes.Block import Block
from mock import *
import time

from Classes.Transaction import Transaction

mock_time = Mock()
mock_time.return_value = 1234567890


class BlockTestCase(unittest.TestCase):
    @patch('time.time_ns', mock_time)
    def test_the_hash_of_the_block_is_calculated_correctly(self):
        block = Block(['test_transaction'], 0)
        self.assertEqual('6ac7374512ebb1a0bca202ff7e138bb34f6edfae3936c4911da4c58399f97ee9', block.calculate_hash())

    def test_the_hash_of_the_block_is_calculated_automatically(self):
        transaction = Transaction('test_sender', 'test_recipient', 100)
        block = Block([transaction], 0)

        self.assertTrue(block.hash is not None)

    @patch('time.time_ns', mock_time)
    def test_the_properties_of_a_block_are_set_correctly(self):
        transaction = Transaction('test_sender', 'test_recipient', 100)
        block = Block([transaction], 1)

        self.assertEqual([transaction], block.transactions)
        self.assertEqual(1234567890, block.timestamp)
        self.assertEqual(1, block.previous_hash)
        self.assertEqual(0, block.nonce)
