import hashlib
import time


class TransactionOutput(object):
    def __init__(self, address: str, amount: int, mode: str = "normal"):
        self.address = address
        self.amount = amount
        self.mode = mode
        self.time = time.time_ns()
        self.id = self.generate_id()

    def generate_id(self) -> str:
        sha = hashlib.sha256()
        sha.update(self.get_id_value_string().encode('utf-8'))
        return sha.hexdigest()

    def get_id_value_string(self) -> str:
        return str(self.address) + " " \
               + str(self.amount) + " " \
               + str(self.mode) + " " + \
               str(self.time)

    def __str__(self) -> str:
        return str(self.id) + ": " \
               + self.get_id_value_string()

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "address": self.address,
            "amount": self.amount,
            "mode": self.mode,
            "time": self.time
        }
