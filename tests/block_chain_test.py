import unittest
from mock import *

from Classes.block import Block
from Classes.block_chain import BlockChain
from Classes.transaction import Transaction
from Classes.transaction_input import TransactionInput
from Classes.transaction_output import TransactionOutput

mock_time = Mock()
mock_time.return_value = 1234567890

sample_transaction_output = TransactionOutput('address1', 1)
sample_transaction_input = TransactionInput(sample_transaction_output)

sample_transaction = Transaction([sample_transaction_input], [sample_transaction_output])


class BlockChainTestCase(unittest.TestCase):
    def test_the_chain_has_a_empty_list_of_transactions_on_initialization(self):
        blockchain = BlockChain()
        self.assertEqual(blockchain.transactions, [])

    def test_the_chain_has_a_empy_list_of_transaction_output_pool_on_initialization(self):
        block_chain = BlockChain()
        self.assertEqual(block_chain.transaction_output_pool, [])

    def test_the_difficulty_is_set_correctly(self):
        block_chain = BlockChain()
        self.assertTrue(block_chain.difficulty == 2)

    def test_the_chain_generates_a_genesis_block_on_init(self):
        block_chain = BlockChain()
        self.assertTrue(len(block_chain.chain) == 1)

    def test_a_genesis_block_is_added_to_the_chain(self):
        block_chain = BlockChain()
        block_chain.create_genesis_block()

        self.assertTrue(len(block_chain.chain) == 1)

    def test_the_chain_resets_when_a_genesis_block_is_created(self):
        block_chain = BlockChain()
        block_chain.add_block()
        block_chain.create_genesis_block()

        self.assertTrue(len(block_chain.chain) == 1)

    def test_a_genesis_block_is_created_correctly(self):
        block_chain = BlockChain()
        genesis_block = block_chain.get_genesis_block()

        self.assertTrue(genesis_block.previous_hash == '0000')
        self.assertTrue(genesis_block.hash is not None)

    def test_a_genesis_block_has_no_transaction(self):
        block_chain = BlockChain()
        block_chain.create_genesis_block()

        self.assertTrue(len(block_chain.chain[0].transactions) == 0)

    def test_the_chain_returns_the_correct_genesis_block(self):
        block_chain = BlockChain()
        genesis_block = block_chain.get_genesis_block()

        self.assertTrue(block_chain.chain[0] == genesis_block)

    def test_the_chain_returns_the_correct_last_block(self):
        block_chain = BlockChain()
        block_chain.add_block()
        last_block = block_chain.get_last_block()

        self.assertTrue(block_chain.chain[-1] == last_block)

    @patch('time.time_ns', mock_time)
    def test_when_a_block_is_added_the_previous_hash_is_set(self):
        block_chain = BlockChain()
        block_chain.transactions = ['test_transactions']
        block_chain.add_block()

        self.assertTrue(block_chain.chain[-1].previous_hash == block_chain.chain[-2].hash)

    def test_when_a_block_is_added_the_hash_is_calculated(self):
        block_chain = BlockChain()
        block_chain.add_block()

        self.assertTrue(block_chain.chain[-1].hash is not None)

    def test_when_a_block_is_added_the_hash_is_correct(self):
        block_chain = BlockChain()
        block_chain.add_block()

        self.assertTrue(block_chain.chain[-1].hash == block_chain.chain[-1].calculate_hash())

    def test_when_a_block_is_added_its_mined_correctly(self):
        block_chain = BlockChain()
        block_chain.add_block()

        self.assertTrue(block_chain.chain[-1].hash.startswith('0' * block_chain.difficulty))

    def test_the_pending_transactions_will_be_removed_when_a_block_is_mined(self):
        block_chain = BlockChain()
        block_chain.transactions = ['test_transactions']
        added_block = block_chain.add_block()

        self.assertIsNotNone(added_block)
        self.assertEqual(block_chain.transactions, [])

    def test_the_transaction_output_pool_will_be_cleared_when_a_block_is_mined(self):
        block_chain = BlockChain()
        block_chain.transaction_output_pool = ['test_utxo']
        added_block = block_chain.add_block()

        self.assertIsNotNone(added_block)
        self.assertEqual(block_chain.transaction_output_pool, [])

    def test_the_chain_returns_the_correct_block(self):
        block_chain = BlockChain()
        block_chain.add_block()
        block = block_chain.get_block(block_chain.chain[-1].hash)

        self.assertTrue(block_chain.chain[-1] == block)

    def test_the_chain_returns_none_when_a_block_is_not_found(self):
        block_chain = BlockChain()
        block_chain.add_block()
        block = block_chain.get_block('test_hash')

        self.assertTrue(block is None)

    def test_the_chain_can_add_a_transaction(self):
        block_chain = BlockChain()
        block_chain.add_transaction(sample_transaction)

        self.assertTrue(len(block_chain.transactions) == 1)
        self.assertEqual(block_chain.transactions[0], sample_transaction)

    def test_the_chain_can_add_a_transaction_output_to_the_pool(self):
        block_chain = BlockChain()
        block_chain.add_transaction(sample_transaction)

        self.assertTrue(len(block_chain.transaction_output_pool) == 1)
        self.assertEqual(block_chain.transaction_output_pool[0], sample_transaction_output)

    @patch('time.time_ns', mock_time)
    def test_the_chain_returns_valid_when_the_chain_is_valid(self):
        block_chain = BlockChain()
        block_chain.transactions = [sample_transaction]

        block_chain.add_block()

        self.assertTrue(block_chain.is_valid())

    @patch('time.time_ns', mock_time)
    def test_the_chain_returns_invalid_when_the_chain_is_invalid_caused_wrong_hash(self):
        block_chain = BlockChain()
        block_chain.transactions = ['test_transactions']

        block_chain.add_block()
        block_chain.chain[1].hash = 'test_hash'

        self.assertFalse(block_chain.is_valid())

    @patch('time.time_ns', mock_time)
    def test_the_chain_returns_invalid_when_the_chain_is_invalid_caused_wrong_previous_hash(self):
        block_chain = BlockChain()
        block_chain.transactions = ['test_transactions']

        block_chain.add_block()
        block_chain.chain[1].previous_hash = 'test_hash'
        block_chain.chain[1].hash = block_chain.chain[1].calculate_hash()

        self.assertFalse(block_chain.is_valid())

    def test_the_chain_can_get_a_transaction_output_from_the_chain(self):
        block_chain = BlockChain()
        block_chain.add_transaction(sample_transaction)
        block_chain.add_block()

        self.assertEqual(block_chain.get_transaction_output(sample_transaction_output.id), sample_transaction_output)

    def test_the_chain_can_get_a_transaction_output_from_the_transaction_output_pool(self):
        block_chain = BlockChain()
        block_chain.transaction_output_pool = [sample_transaction_output]

        self.assertEqual(block_chain.get_transaction_output(sample_transaction_output.id), sample_transaction_output)

    def test_the_chain_returns_none_when_a_transaction_output_is_not_found(self):
        block_chain = BlockChain()

        self.assertEqual(block_chain.get_transaction_output('test_id'), None)

    def test_the_chain_can_get_a_balance_from_a_address_when_there_are_blocks_with_transactions(self):
        block_chain = BlockChain()
        block_chain.create_genesis_block()

        mined_transaction_plus_5 = Transaction([], [TransactionOutput('address2', 5)])
        mined_transaction_minus_3 = Transaction([TransactionInput(TransactionOutput('address2', 3))], [])
        pending_transaction_plus_2 = Transaction([], [TransactionOutput('address2', 2)])
        pending_transaction_minus_1 = Transaction([TransactionInput(TransactionOutput('address2', 1))], [])

        block_chain.add_transaction(mined_transaction_plus_5)
        block_chain.add_transaction(mined_transaction_minus_3)
        block_chain.add_block()

        block_chain.add_transaction(pending_transaction_plus_2)
        block_chain.add_transaction(pending_transaction_minus_1)

        self.assertEqual(block_chain.get_balance('address2'), 3)

    def test_the_blocks_can_be_received_from_a_specific_height(self):
        block_chain = BlockChain()
        block_chain.create_genesis_block()
        block_chain.add_block()
        expected_block_1 = block_chain.add_block()
        expected_block_2 = block_chain.add_block()

        received_blocks = block_chain.get_blocks_from_height(2)

        self.assertEqual(len(received_blocks), 2)
        self.assertEqual(received_blocks[0], expected_block_1)
        self.assertEqual(received_blocks[1], expected_block_2)

    def test_a_block_can_not_be_added_to_the_chain_from_a_dict_when_a_transaction_is_invalid(self):
        block_chain = BlockChain()
        block_chain.create_genesis_block()
        block_chain.add_block()

        block = Block([sample_transaction], block_chain.chain[-1].hash)
        block_dict = block.__dict__()
        block_dict['transactions'][0]['inputs'][0]['transaction_output_id'] = 'test_id'

        self.assertFalse(block_chain.add_block_from_dict(block_dict))

    def test_a_block_can_be_added_to_the_chain_from_a_dict_when_its_transactions_are_valid(self):
        block_chain = BlockChain()
        block_chain.create_genesis_block()
        block_chain.add_block()
        block_chain.add_transaction(sample_transaction)

        block = Block([sample_transaction], block_chain.chain[-1].hash)
        block_dict = block.__dict__()

        self.assertTrue(block_chain.add_block_from_dict(block_dict))
