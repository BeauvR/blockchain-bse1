from __future__ import annotations

import hashlib
import time

from typing import List

from Classes.transaction_input import TransactionInput
from Classes.transaction_output import TransactionOutput


class Transaction(object):

    def __init__(self, inputs: List[TransactionInput], outputs: List[TransactionOutput]):
        self.inputs = inputs
        self.outputs = outputs
        self.time = time.time_ns()
        self.id = self.generate_id()

    def inputs_to_string(self) -> str:
        string = ""
        for input in self.inputs:
            string += str(input) + ", "
        return string

    def outputs_to_string(self) -> str:
        string = ""
        for output in self.outputs:
            string += str(output) + ", "
        return string

    def generate_id(self) -> str:
        sha = hashlib.sha256()
        sha.update(self.get_id_value_string().encode('utf-8'))
        return sha.hexdigest()

    def get_fee(self) -> int:
        input_sum = 0
        output_sum = 0

        for input in self.inputs:
            input_sum += input.transaction_output.amount

        for output in self.outputs:
            if output.mode != "normal":
                return 0
            else:
                output_sum += output.amount

        if input_sum - output_sum < 0:
            return 0

        return input_sum - output_sum

    def has_fee_transaction_output(self) -> bool:
        for output in self.outputs:
            if output.mode == "fee":
                return True
        return False

    def add_fee_transaction_output(self, address: str) -> TransactionOutput | None:
        if self.has_fee_transaction_output():
            return None

        fee = self.get_fee()
        transaction_output = TransactionOutput(address, fee, "fee")
        self.outputs.append(transaction_output)

        return transaction_output

    def get_fee_transaction_output(self) -> TransactionOutput | None:
        for output in self.outputs:
            if output.mode == "fee":
                return output
        return None

    def get_id_value_string(self) -> str:
        return self.inputs_to_string() + " -> " + self.outputs_to_string()

    def __str__(self) -> str:
        return str(self.id) + ": " + self.get_id_value_string()

    def inputs_to_dict(self) -> List[dict]:
        transaction_inputs = []
        for transaction_input in self.inputs:
            transaction_inputs.append(transaction_input.__dict__())
        return transaction_inputs

    def outputs_to_dict(self) -> List[dict]:
        outputs = []
        for output in self.outputs:
            outputs.append(output.__dict__())
        return outputs

    def __dict__(self) -> dict:
        return {
            "inputs": self.inputs_to_dict(),
            "outputs": self.outputs_to_dict(),
            "time": self.time,
            "id": self.id
        }
