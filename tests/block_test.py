import unittest

from Classes.Block import Block
from mock import *
import time

mock_time = Mock()
mock_time.return_value = 1234567890


class BlockTestCase(unittest.TestCase):
    @patch('time.time_ns', mock_time)
    def test_the_hash_of_the_block_is_calculated_correctly(self):
        block = Block(['test_transactions'], 0)
        self.assertEqual('ee7ffcbee789fd0c1a3491872d11ffdb50c2a607f535795482589c28d86af69a', block.calculate_hash())

    def test_the_hash_of_the_block_is_calculated_automatically(self):
        block = Block(['test_transactions'], 0)

        self.assertTrue(block.hash is not None)


if __name__ == '__main__':
    unittest.main()
