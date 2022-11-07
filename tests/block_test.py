import unittest

from Classes.block import Block
from mock import *

from Classes.transaction import Transaction
from Classes.transaction_input import TransactionInput
from Classes.transaction_output import TransactionOutput

mock_time = Mock()
mock_time.return_value = 1234567890

sample_transaction_output_1 = TransactionOutput('address1', 1)
sample_transaction_input_1 = TransactionInput(sample_transaction_output_1)

sample_transaction_output_2 = TransactionOutput('address2', 2)
sample_transaction_input_2 = TransactionInput(sample_transaction_output_2)

sample_transaction_1 = Transaction([sample_transaction_input_1], [sample_transaction_output_1])
sample_transaction_2 = Transaction([sample_transaction_input_2], [sample_transaction_output_2])


class BlockTestCase(unittest.TestCase):

    @patch('time.time_ns', mock_time)
    def test_the_properties_of_a_block_are_set_correctly(self):
        block = Block([sample_transaction_1, sample_transaction_2], '0000')

        self.assertEqual([sample_transaction_1, sample_transaction_2], block.transactions)
        self.assertEqual(1234567890, block.timestamp)
        self.assertEqual('0000', block.previous_hash)
        self.assertEqual(0, block.nonce)

    def test_the_hash_of_the_block_is_calculated_automatically(self):
        block = Block([sample_transaction_1, sample_transaction_2], '0000')

        self.assertTrue(block.hash is not None)

    @patch('time.time_ns', mock_time)
    def test_the_id_value_string_is_correctly_generated(self):
        block = Block([sample_transaction_1, sample_transaction_2], '0000')
        self.assertEqual(
            '1234567890, ' + block.transactions_to_string() + ', 0000, 0',
            block.get_id_value_string()
        )

    @patch('time.time_ns', mock_time)
    def test_the_hash_of_the_block_is_calculated_correctly(self):
        block = Block([], '0000')
        self.assertEqual('a175f2db66c0ab7bddb191621be683192b92592302969a4e8090563ae94ec3bd', block.calculate_hash())

    def test_the_transactions_will_be_converted_to_a_string_correctly(self):
        block = Block([sample_transaction_1, sample_transaction_2], '0000')
        self.assertEqual(
            str(sample_transaction_1) + ', ' + str(sample_transaction_2) + ', ',
            block.transactions_to_string()
        )

    def test_the_block_can_be_mined_correctly(self):
        block = Block([sample_transaction_1, sample_transaction_2], '0000')
        block.mine(3)

        self.assertEqual('000', block.hash[:3])

    def test_when_a_block_is_transformed_to_a_string_it_should_return_the_correct_string(self):
        block = Block([sample_transaction_1, sample_transaction_2], '0000')
        self.assertEqual(
            block.hash + ': ' + block.get_id_value_string(),
            str(block)
        )

    def test_a_block_correctly_transforms_transactions_to_a_dicts(self):
        block = Block([sample_transaction_1, sample_transaction_2], '0000')
        self.assertEqual(
            [sample_transaction_1.__dict__(), sample_transaction_2.__dict__()],
            block.transactions_to_dict()
        )

    def test_a_block_correctly_transforms_to_a_dict(self):
        block = Block([sample_transaction_1, sample_transaction_2], '0000')
        self.assertEqual(
            {
                'hash': block.hash,
                'timestamp': block.timestamp,
                'transactions': block.transactions_to_dict(),
                'previous_hash': block.previous_hash,
                'nonce': block.nonce
            },
            block.__dict__()
        )
