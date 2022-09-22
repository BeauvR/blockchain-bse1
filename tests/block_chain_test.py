import unittest
from mock import *
import time

from Classes.Block import Block
from Classes.BlockChain import BlockChain

mock_time = Mock()
mock_time.return_value = 1234567890


class BlockChainTestCase(unittest.TestCase):
    def test_the_chain_has_a_empty_list_of_transactions_on_initialization(self):
        blockchain = BlockChain()
        self.assertEqual(blockchain.transactions, [])

    def test_the_difficulty_is_set_correctly(self):
        block_chain = BlockChain()
        self.assertTrue(block_chain.difficulty == 2)

    def test_the_chain_generates_a_genesis_block_on_init(self):
        block_chain = BlockChain()
        self.assertTrue(len(block_chain.chain) == 1)

    def test_a_genesis_block_is_created_correctly(self):
        block_chain = BlockChain()
        genesis_block = block_chain.get_genesis_block()

        self.assertTrue(genesis_block.previous_hash == 0)
        self.assertTrue(genesis_block.hash is not None)

    def test_a_genesis_block_is_added_to_the_chain(self):
        block_chain = BlockChain()
        block_chain.create_genesis_block()

        self.assertTrue(len(block_chain.chain) == 1)

    def test_the_chain_resets_when_a_genesis_block_is_created(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])
        block_chain.create_genesis_block()

        self.assertTrue(len(block_chain.chain) == 1)

    def test_the_chain_returns_the_correct_genesis_block(self):
        block_chain = BlockChain()
        genesis_block = block_chain.get_genesis_block()

        self.assertTrue(block_chain.chain[0] == genesis_block)

    def test_the_chain_returns_the_correct_last_block(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])
        last_block = block_chain.get_last_block()

        self.assertTrue(block_chain.chain[-1] == last_block)

    @patch('time.time_ns', mock_time)
    def test_when_a_block_is_added_the_previous_hash_is_set(self):
        block_chain = BlockChain()
        block_chain.transactions = ['test_transactions']
        block_chain.add_block(6)

        self.assertTrue(block_chain.chain[-1].previous_hash == block_chain.chain[-2].hash)

    def test_when_a_block_is_added_the_hash_is_calculated(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])

        self.assertTrue(block_chain.chain[-1].hash is not None)

    def test_when_a_block_is_added_the_hash_is_correct(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])

        self.assertTrue(block_chain.chain[-1].hash == block_chain.chain[-1].calculate_hash())

    def test_a_block_could_not_be_added_the_the_chain_with_a_invalid_nonce(self):
        block_chain = BlockChain()
        block_chain.transactions = ['test_transactions']
        added_block = block_chain.add_block(0)

        self.assertIsNone(added_block)
        self.assertEqual(block_chain.transactions, ['test_transactions'])

    @patch('time.time_ns', mock_time)
    def test_a_block_could_be_added_to_the_chain_when_the_nonce_is_valid(self):
        block_chain = BlockChain()
        block_chain.transactions = ['test_transactions']

        # Previous calculated nonce and 6 is the correct for difficulty 2
        block = block_chain.add_block(6)

        self.assertIsNotNone(block)
        self.assertTrue(len(block_chain.chain) == 2)
        self.assertEqual(block_chain.transactions, [])

    def test_the_chain_returns_the_correct_block(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])
        block = block_chain.get_block(block_chain.chain[-1].hash)

        self.assertTrue(block_chain.chain[-1] == block)

    def test_the_chain_returns_none_when_a_block_is_not_found(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])
        block = block_chain.get_block('test_hash')

        self.assertTrue(block is None)

    def test_the_chain_can_add_a_transaction(self):
        block_chain = BlockChain()
        transaction = block_chain.add_transaction('test_sender', 'test_recipient', 100)

        self.assertTrue(len(block_chain.transactions) == 1)
        self.assertEqual(block_chain.transactions[0], transaction)
