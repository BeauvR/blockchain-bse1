from __future__ import annotations

import hashlib
import time
from typing import List

from Classes.transaction import Transaction


class Block(object):
    def __init__(self, transactions: List[Transaction], previous_hash: str):
        self.timestamp = time.time_ns()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def get_id_value_string(self) -> str:
        return str(self.timestamp) + ", " \
               + self.transactions_to_string() + ", " \
               + str(self.previous_hash) + ", " \
               + str(self.nonce)

    def calculate_hash(self) -> str:
        sha = hashlib.sha256()
        sha.update(self.get_id_value_string().encode('utf-8'))
        return sha.hexdigest()

    def transactions_to_string(self) -> str:
        string = ""
        for transaction in self.transactions:
            string += str(transaction) + ", "
        return string

    def mine(self, difficulty: int) -> None:
        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()

        return None

    @staticmethod
    def from_dict(block_dict: dict) -> Block:
        transactions = []
        for transaction_dict in block_dict["transactions"]:
            transaction = Transaction([], [])
            transactions.append(transaction.from_dict(transaction_dict))
        block = Block(transactions, block_dict["previous_hash"])
        block.timestamp = block_dict["timestamp"]
        block.nonce = block_dict["nonce"]
        block.hash = block_dict["hash"]

        return block

    def __str__(self) -> str:
        return str(self.hash) + ": " + self.get_id_value_string()

    def transactions_to_dict(self) -> List[dict]:
        transactions = []
        for transaction in self.transactions:
            transactions.append(transaction.__dict__())
        return transactions

    def __dict__(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "transactions": self.transactions_to_dict(),
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
