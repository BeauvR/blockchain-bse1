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
        block = Block(['test_transaction'], 0, 1)
        self.assertEqual('21f4104611f822526b8807eac16c22346cae1a48ce90777bbd2363af96ad979d', block.calculate_hash())

    def test_the_hash_of_the_block_is_calculated_automatically(self):
        transaction = Transaction('test_sender', 'test_recipient', 100)
        block = Block([transaction], 0, 1)

        self.assertTrue(block.hash is not None)

    @patch('time.time_ns', mock_time)
    def test_the_properties_of_a_block_are_set_correctly(self):
        transaction = Transaction('test_sender', 'test_recipient', 100)
        block = Block([transaction], 1, 2)

        self.assertEqual([transaction], block.transactions)
        self.assertEqual(1234567890, block.timestamp)
        self.assertEqual(1, block.previous_hash)
        self.assertEqual(2, block.nonce)
