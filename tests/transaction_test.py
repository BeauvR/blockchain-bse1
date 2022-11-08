import unittest

from mock import *

from Classes.block_chain import BlockChain
from Classes.transaction import Transaction
from Classes.transaction_input import TransactionInput
from Classes.transaction_output import TransactionOutput

mock_time = Mock()
mock_time.return_value = 1234567890

block_chain = BlockChain()

sample_transaction_output = TransactionOutput('address', 1)
sample_transaction_input = TransactionInput(sample_transaction_output)


class TransactionTestCase(unittest.TestCase):
    def test_the_properties_from_the_transaction_are_correctly_set(self):
        transaction = Transaction([sample_transaction_input], [sample_transaction_output])
        self.assertEqual([sample_transaction_input], transaction.inputs)
        self.assertEqual([sample_transaction_output], transaction.outputs)

    @patch('time.time_ns', mock_time)
    def test_the_transaction_automatically_get_the_current_timestamp(self):
        transaction = Transaction([sample_transaction_input], [sample_transaction_output])
        self.assertEqual(1234567890, transaction.time)

    @patch('time.time_ns', mock_time)
    def test_the_id_should_be_generated_automatically(self):
        transaction = Transaction([sample_transaction_input], [sample_transaction_output])
        self.assertTrue(isinstance(transaction.id, str))

    @patch('time.time_ns', mock_time)
    def test_the_inputs_should_be_converted_to_a_string_correctly(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction = Transaction([transaction_input1, transaction_input2], [sample_transaction_output])
        self.assertEqual(
            str(transaction_input1) + ', ' + str(transaction_input2) + ', ',
            transaction.inputs_to_string()
        )

    @patch('time.time_ns', mock_time)
    def test_the_outputs_should_be_converted_to_a_string_correctly(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_output2 = TransactionOutput('address2', 2)

        transaction = Transaction([sample_transaction_input], [transaction_output1, transaction_output2])
        self.assertEqual(
            str(transaction_output1) + ', ' + str(transaction_output2) + ', ',
            transaction.outputs_to_string()
        )

    def test_the_transaction_fee_should_be_calculated_correctly(self):
        transactionInput = TransactionInput(TransactionOutput('address1', 4))
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_output2 = TransactionOutput('address2', 2)

        transaction = Transaction([transactionInput], [transaction_output1, transaction_output2])
        self.assertEqual(1, transaction.get_fee())

    def test_the_transaction_fee_should_be_zero_if_no_inputs_are_given(self):
        transaction = Transaction([], [sample_transaction_output])
        self.assertEqual(0, transaction.get_fee())

    def test_the_transaction_fee_should_be_zero_if_no_inputs_and_outputs_are_given(self):
        transaction = Transaction([], [])
        self.assertEqual(0, transaction.get_fee())

    def test_the_transaction_fee_should_be_zero_if_there_is_no_difference_between_inputs_and_outputs(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output1, transaction_output2])
        self.assertEqual(0, transaction.get_fee())

    def test_the_transaction_fee_should_be_zero_if_the_inputs_are_bigger_than_the_outputs(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 3)
        transaction_output4 = TransactionOutput('address4', 4)

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3, transaction_output4])
        self.assertEqual(0, transaction.get_fee())

    def test_the_transaction_fee_should_be_zero_when_there_is_a_fee_transaction_output(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2, 'fee')

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])
        self.assertEqual(0, transaction.get_fee())

    def test_the_has_fee_transaction_output_should_return_true_if_there_is_a_fee_transaction_output(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2, 'fee')

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])
        self.assertTrue(transaction.has_fee_transaction_output())

    def test_the_has_fee_transaction_output_should_return_false_if_there_is_no_fee_transaction_output(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2)

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])
        self.assertFalse(transaction.has_fee_transaction_output())

    def test_it_is_not_possible_to_create_a_fee_transaction_output_when_there_is_already_a_fee_transaction_output(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2, 'fee')

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        new_fee_transaction_output = transaction.add_fee_transaction_output('address4')

        self.assertIsNone(new_fee_transaction_output)

    def test_it_is_possible_to_create_a_fee_transaction_output_when_there_is_no_fee_transaction_output(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2)

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        new_fee_transaction_output = transaction.add_fee_transaction_output('address4')

        self.assertEqual('address4', new_fee_transaction_output.address)
        self.assertEqual(1, new_fee_transaction_output.amount)
        self.assertEqual('fee', new_fee_transaction_output.mode)

    def test_it_is_possible_to_receive_the_fee_transaction_output(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2)

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        new_fee_transaction_output = transaction.add_fee_transaction_output('address4')

        self.assertEqual(new_fee_transaction_output, transaction.get_fee_transaction_output())

    def test_when_a_fee_transaction_output_is_not_created_it_should_return_none(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2)

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertIsNone(transaction.get_fee_transaction_output())

    def test_it_is_invalid_when_the_input_has_no_transaction_output(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2)

        transaction_input1.transaction_output = None

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain.transaction_output_pool))

    def test_it_is_invalid_when_the_input_has_a_transaction_output_that_is_not_in_the_transaction_output_pool(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2)

        block_chain.transaction_output_pool = []
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain))

    def test_it_is_valid_when_the_input_has_a_transaction_output_that_is_in_the_transaction_output_pool(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertTrue(transaction.is_valid(block_chain))

    def test_it_is_invalid_when_the_input_signature_is_invalid(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 2)

        transaction_input1.signature = 'invalid_signature'

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain))

    def test_it_is_invalid_when_a_transaction_output_two_times_is_used_as_input(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_input2 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address3', 2)

        block_chain.transaction_output_pool = [transaction_output1]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output2])

        self.assertFalse(transaction.is_valid(block_chain))
    def test_it_is_invalid_when_the_output_amount_is_zero(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 0)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain))

    def test_it_is_invalid_when_the_output_amount_is_negative(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', -1)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain))

    def test_it_is_invalid_when_the_total_input_amount_is_below_zero(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', -2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 3)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain))

    def test_it_is_invalid_when_the_total_input_amount_is_zero(self):
        transaction_output1 = TransactionOutput('address1', -1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 0)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 1)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain))

    def test_it_is_invalid_when_the_total_output_amount_is_below_zero(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', -3)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain))

    def test_it_is_invalid_when_the_total_output_amount_is_zero(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 0)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain))

    def test_it_is_invalid_when_the_total_input_amount_is_lower_than_the_total_output_amount(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 1)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 3)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertFalse(transaction.is_valid(block_chain))

    def test_it_is_valid_when_all_requirements_are_met_and_the_totals_are_equal(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 2)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 3)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertTrue(transaction.is_valid(block_chain))

    def test_it_is_valid_when_all_requirements_are_met_and_the_input_total_is_higher_than_the_output_total(self):
        transaction_output1 = TransactionOutput('address1', 1)
        transaction_input1 = TransactionInput(transaction_output1)

        transaction_output2 = TransactionOutput('address2', 1)
        transaction_input2 = TransactionInput(transaction_output2)

        transaction_output3 = TransactionOutput('address3', 1)

        block_chain.transaction_output_pool = [transaction_output1, transaction_output2]
        block_chain.chain = []

        transaction = Transaction([transaction_input1, transaction_input2], [transaction_output3])

        self.assertTrue(transaction.is_valid(block_chain))

    def test_a_transaction_correctly_transforms_itself_to_a_string(self):
        transaction = Transaction([sample_transaction_input], [sample_transaction_output])
        self.assertEqual(
            transaction.id + ': ' + transaction.inputs_to_string() + ' -> ' + transaction.outputs_to_string(),
            str(transaction)
        )

    def test_a_transaction_correctly_transforms_inputs_to_a_dict(self):
        transaction = Transaction([sample_transaction_input, sample_transaction_input], [])

        self.assertEqual([
            sample_transaction_input.__dict__(),
            sample_transaction_input.__dict__()
        ], transaction.inputs_to_dict())

    def test_a_transaction_correctly_transforms_outputs_to_a_dict(self):
        transaction = Transaction([], [sample_transaction_output, sample_transaction_output])

        self.assertEqual([
            sample_transaction_output.__dict__(),
            sample_transaction_output.__dict__()
        ], transaction.outputs_to_dict())

    def test_a_transaction_correctly_transforms_itself_to_a_dict(self):
        transaction = Transaction([sample_transaction_input], [sample_transaction_output])
        self.assertEqual(
            {
                'id': transaction.id,
                'inputs': transaction.inputs_to_dict(),
                'outputs': transaction.outputs_to_dict(),
                'time': transaction.time
            },
            transaction.__dict__()
        )
