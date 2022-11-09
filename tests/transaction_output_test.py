import unittest

from mock import *

from Classes.transaction_output import TransactionOutput

mock_time = Mock()
mock_time.return_value = 1234567890


class TransactionOutputTestCase(unittest.TestCase):
    def test_the_properties_from_the_transaction_output_are_correctly_set(self):
        transaction_output = TransactionOutput('address1', 1)
        self.assertEqual('address1', transaction_output.address)
        self.assertEqual(1, transaction_output.amount)

    def test_the_transaction_output_mode_is_automatically_set(self):
        transaction_output = TransactionOutput('address1', 1)
        self.assertEqual('normal', transaction_output.mode)

    def test_the_transaction_output_mode_can_be_set_to_fee(self):
        transaction_output = TransactionOutput('address1', 1, 'fee')
        self.assertEqual('fee', transaction_output.mode)

    @patch('time.time_ns', mock_time)
    def test_the_transaction_output_automatically_get_the_current_timestamp(self):
        transaction_output = TransactionOutput('address1', 1)
        self.assertEqual(1234567890, transaction_output.time)

    def test_the_transaction_output_id_should_be_generated_automatically(self):
        transaction_output = TransactionOutput('address1', 1)
        self.assertTrue(isinstance(transaction_output.id, str))

    def test_a_transaction_output_can_be_made_from_a_dict(self):
        transaction_output = TransactionOutput.from_dict({
            'address': 'address1',
            'amount': 1,
            'mode': 'normal',
            'time': 1234567890,
            'id': 'test_id'
        })
        self.assertEqual('address1', transaction_output.address)
        self.assertEqual(1, transaction_output.amount)
        self.assertEqual('normal', transaction_output.mode)
        self.assertEqual(1234567890, transaction_output.time)
        self.assertEqual('test_id', transaction_output.id)

    @patch('time.time_ns', mock_time)
    def test_a_transaction_output_correctly_transforms_itself_to_a_string(self):
        transaction_output = TransactionOutput('address1', 1)

        self.assertEqual(transaction_output.id + ': address1 1 normal 1234567890', str(transaction_output))

    @patch('time.time_ns', mock_time)
    def test_a_transaction_output_correctly_transforms_itself_to_a_dict(self):
        transaction_output = TransactionOutput('address1', 1)

        self.assertEqual({
            'id': transaction_output.id,
            'address': 'address1',
            'amount': 1,
            'mode': 'normal',
            'time': 1234567890
        }, transaction_output.__dict__())
