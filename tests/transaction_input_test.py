import unittest

from mock import *

from Classes.transaction_input import TransactionInput
from Classes.transaction_output import TransactionOutput

mock_time = Mock()
mock_time.return_value = 1234567890

sample_transaction_output = TransactionOutput('address', 1)


class TransactionInputTestCase(unittest.TestCase):
    def test_the_properties_from_the_transaction_input_are_correctly_set(self):
        transaction_input = TransactionInput(sample_transaction_output)
        self.assertEqual(sample_transaction_output, transaction_input.transaction_output)

    def test_the_transaction_input_signature_is_not_automatically_set(self):
        transaction_input = TransactionInput(sample_transaction_output)
        self.assertIsNone(transaction_input.signature)

    @patch('time.time_ns', mock_time)
    def test_the_transaction_input_automatically_get_the_current_timestamp(self):
        transaction_input = TransactionInput(sample_transaction_output)
        self.assertEqual(1234567890, transaction_input.time)

    def test_the_transaction_input_id_should_be_generated_automatically(self):
        transaction_input = TransactionInput(sample_transaction_output)
        self.assertTrue(isinstance(transaction_input.id, str))

    def test_the_transaction_input_signature_can_be_set(self):
        transaction_input = TransactionInput(sample_transaction_output)
        transaction_input.set_signature('test_signature')
        self.assertEqual('test_signature', transaction_input.signature)

    def test_the_transaction_input_signature_verify_method_returns_true_when_a_signature_is_not_set(self):
        transaction_input = TransactionInput(sample_transaction_output)
        self.assertTrue(transaction_input.verify_signature('test_key'))

    def test_the_transaction_input_signature_verify_method_returns_false_when_a_signature_is_set(self):
        transaction_input = TransactionInput(sample_transaction_output)
        transaction_input.set_signature('test_signature')
        self.assertFalse(transaction_input.verify_signature('test_key'))

    def test_a_transaction_input_can_be_made_from_a_dict(self):
        transaction_input = TransactionInput.from_dict({
            'transaction_output': {
                'address': 'address1',
                'amount': 1,
                'mode': 'normal',
                'time': 1234567890,
                'id': 'test_id'
            },
            'signature': 'test_signature',
            'time': 1234567890,
            'id': 'test_id'
        })
        self.assertIsNotNone(transaction_input.transaction_output)
        self.assertEqual('test_signature', transaction_input.signature)
        self.assertEqual(1234567890, transaction_input.time)
        self.assertEqual('test_id', transaction_input.id)

    @patch('time.time_ns', mock_time)
    def test_a_transaction_input_correctly_transforms_itself_to_a_string(self):
        transaction_input = TransactionInput(sample_transaction_output)

        self.assertEqual(
            transaction_input.id + ': 1234567890 ' + str(sample_transaction_output),
            str(transaction_input)
        )

    @patch('time.time_ns', mock_time)
    def test_a_transaction_input_correctly_transforms_itself_to_a_dict(self):
        transaction_input = TransactionInput(sample_transaction_output)

        self.assertEqual({
            'id': transaction_input.id,
            'time': 1234567890,
            'signature': None,
            'transaction_output': sample_transaction_output.__dict__()
        }, transaction_input.__dict__())
