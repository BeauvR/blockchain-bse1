import hashlib
import time

from Classes.transaction_output import TransactionOutput


class TransactionInput(object):

    def __init__(self, transaction_output: TransactionOutput):
        self.transaction_output = transaction_output
        self.signature = None
        self.time = time.time_ns()
        self.id = self.generate_id()

    def generate_id(self) -> str:
        sha = hashlib.sha256()
        sha.update(self.get_id_value_string().encode('utf-8'))
        return sha.hexdigest()

    def set_signature(self, signature: str) -> None:
        self.signature = signature

    def verify_signature(self, public_key) -> bool:
        if not self.signature:
            return False

        return True

    def get_id_value_string(self) -> str:
        return str(self.time) + " " + str(self.transaction_output)

    def __str__(self) -> str:
        return str(self.id) + ": " + self.get_id_value_string()

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "transaction_output": self.transaction_output.__dict__(),
            "signature": self.signature,
            "time": self.time
        }
