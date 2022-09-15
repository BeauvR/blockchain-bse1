import unittest

from Classes.BlockChain import BlockChain


class BlockChainTestCase(unittest.TestCase):
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

    def test_when_a_block_is_added_the_previous_hash_is_set(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])

        self.assertTrue(block_chain.chain[-1].previous_hash == block_chain.chain[-2].hash)

    def test_when_a_block_is_added_the_hash_is_calculated(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])

        self.assertTrue(block_chain.chain[-1].hash is not None)

    def test_when_a_block_is_added_the_hash_is_correct(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])

        self.assertTrue(block_chain.chain[-1].hash == block_chain.chain[-1].calculate_hash())

    def test_a_block_is_added_to_the_chain(self):
        block_chain = BlockChain()
        block_chain.add_block(['test_transactions'])

        self.assertTrue(len(block_chain.chain) == 2)

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
