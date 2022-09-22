from Classes.Block import Block
from Classes.Transaction import Transaction


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_genesis_block()
        self.difficulty = 2

    def create_genesis_block(self):
        block = Block([], 0, 0)

        self.chain = [block]
        return block

    def get_genesis_block(self):
        return self.chain[0]

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, nonce):
        block = Block(self.transactions, self.get_last_block().hash, nonce)
        block.previous_hash = self.get_last_block().hash
        block.hash = block.calculate_hash()

        if block.hash.startswith('0' * self.difficulty):
            self.chain.append(block)
            self.transactions = []
            return block

        return None

    def get_block(self, block_hash):
        for block in self.chain:
            if block.hash == block_hash:
                return block
        return None

    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        self.transactions.append(transaction)
        return transaction
