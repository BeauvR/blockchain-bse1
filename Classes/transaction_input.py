from __future__ import annotations

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
            return True

        # for testing purposes it returns false when a signature is set, TODO: implement signature verification
        return False

    @staticmethod
    def from_dict(dict_transaction_input: dict) -> TransactionInput:
        transaction_input =  TransactionInput(TransactionOutput.from_dict(dict_transaction_input["transaction_output"]))
        transaction_input.signature = dict_transaction_input["signature"]
        transaction_input.time = dict_transaction_input["time"]
        transaction_input.id = dict_transaction_input["id"]

        return transaction_input

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
