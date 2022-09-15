import hashlib
import time


class Block(object):
    def __init__(self, transactions, previous_hash):
        self.timestamp = time.time_ns()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.timestamp).encode('utf-8') +
            str(self.transactions).encode('utf-8') +
            str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()