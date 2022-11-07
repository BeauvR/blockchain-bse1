from __future__ import annotations

import array
from typing import List

from Classes.block import Block
from Classes.transaction import Transaction
from Classes.transaction_output import TransactionOutput


class BlockChain(object):
    def __init__(self):
        self.chain: List[Block] = []
        self.transactions: List[Transaction] = []
        self.create_genesis_block()
        self.difficulty = 2
        self.transaction_output_pool: List[TransactionOutput] = []

    def create_genesis_block(self) -> None:
        coinbase = Transaction([], [])
        block = Block([coinbase], '0000')

        self.chain = [block]
        return None

    def get_genesis_block(self) -> Block:
        return self.chain[0]

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self) -> Block:
        block = Block(
            self.transactions,
            self.get_last_block().hash
        )

        block.mine(self.difficulty)

        self.chain.append(block)
        self.transactions = []
        self.transaction_output_pool = []
        return block

    def get_block(self, block_hash) -> Block | None:
        for block in self.chain:
            if block.hash == block_hash:
                return block
        return None

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

        for output in transaction.outputs:
            self.transaction_output_pool.append(output)

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_transaction_output(self, transaction_output_id: str) -> TransactionOutput | None:
        for block in self.chain:
            for transaction in block.transactions:
                for output in transaction.outputs:
                    if output.id == transaction_output_id:
                        return output

        for output in self.transaction_output_pool:
            if output.id == transaction_output_id:
                return output

        return None
