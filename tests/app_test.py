from App import app, block_chain as AppBlockChain

import unittest
from mock import *
import time

from Classes.block import Block
from Classes.transaction import Transaction
from Classes.transaction_input import TransactionInput
from Classes.transaction_output import TransactionOutput

mock_time = Mock()
mock_time.return_value = 1234567890

sample_transaction_output = TransactionOutput('address1', 1)
sample_transaction_input = TransactionInput(sample_transaction_output)

sample_transaction = Transaction([sample_transaction_input], [sample_transaction_output])


class AppTestCase(unittest.TestCase):
    def test_the_app_returns_the_correct_difficulty(self):
        client = app.test_client(self)
        response = client.get('/difficulty')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json == AppBlockChain.difficulty)

    def test_when_the_app_runs_a_genesis_block_is_created(self):
        client = app.test_client(self)
        response = client.get('/genesisBlock')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['previous_hash'] == '0000')

    @patch('time.time_ns', mock_time)
    def test_when_the_app_runs_it_returns_the_correct_last_block(self):
        newest_block = Block([sample_transaction], 'previous_hash')
        AppBlockChain.chain.append(newest_block)

        client = app.test_client(self)
        response = client.get('/lastBlock')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['hash'] == newest_block.hash)

    def test_when_the_app_runs_it_returns_the_correct_chain(self):
        # reset the chain for testing
        AppBlockChain.create_genesis_block()
        block = Block([sample_transaction], 'previous_hash')
        AppBlockChain.chain.append(block)

        client = app.test_client(self)
        response = client.get('/chain')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json[0]['previous_hash'] == '0000')
        self.assertTrue(response.json[1]['hash'] == block.hash)

    @patch('time.time_ns', mock_time)
    def test_the_app_can_mine_a_block(self):
        # reset the chain for testing
        AppBlockChain.create_genesis_block()
        AppBlockChain.transactions = [sample_transaction]
        AppBlockChain.transaction_output_pool = [sample_transaction_output]

        client = app.test_client(self)
        response = client.post('/block')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('nonce' in response.json)
        self.assertIsNotNone(response.json['nonce'])
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['hash'] == AppBlockChain.get_last_block().hash)

    def test_the_app_can_get_a_block(self):
        block = Block([sample_transaction], 'previous_hash')
        AppBlockChain.chain.append(block)

        client = app.test_client(self)
        response = client.get('/block/' + block.hash)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['hash'] == block.hash)
        self.assertTrue('transactions' in response.json)
        self.assertIsNotNone(response.json['transactions'])

    def test_the_app_returns_404_when_a_block_is_not_found(self):
        client = app.test_client(self)
        response = client.get('/block/invalid_hash')

        self.assertEqual(response.status_code, 404)

    def test_the_app_returns_a_error_when_there_is_not_a_input(self):
        client = app.test_client(self)
        response = client.post('/transaction',
                               json={'outputs': [{'address': 'address_recipient', 'amount': 50}]})

        self.assertEqual(response.status_code, 400)

    def test_the_app_returns_a_error_when_there_is_a_invalid_input(self):
        client = app.test_client(self)
        response = client.post(
            '/transaction',
            json={
                'inputs': [{'nonce': 'xxxx'}],
                'outputs': [{'address': 'address_recipient', 'amount': '50'}]}
        )
        print(response)

        self.assertEqual(response.status_code, 400)

    def test_the_app_returns_a_error_when_there_is_a_invalid_input_with_unknown_id(self):
        client = app.test_client(self)
        response = client.post(
            '/transaction',
            json={
                'inputs': [{'transaction_output_id': 'xxx'}],
                'outputs': [{'address': 'address_recipient', 'amount': 50}]}
        )

        self.assertEqual(response.status_code, 400)

    def test_the_app_returns_a_error_when_there_is_not_a_output(self):
        client = app.test_client(self)
        response = client.post('/transaction',
                               json={'inputs': [{'transaction_output_id': 'xxxx'}]})

        self.assertEqual(response.status_code, 400)

    def test_the_app_returns_a_error_when_there_is_a_invalid_output(self):
        client = app.test_client(self)
        response = client.post('/transaction',
                               json={
                                   'inputs': [{'transaction_output_id': 'xxxx'}],
                                   'outputs': [{'nonce': 'address_recipient'}]}
                               )

        self.assertEqual(response.status_code, 400)

    def test_the_app_returns_a_error_when_the_transaction_is_not_valid(self):
        AppBlockChain.transaction_output_pool = [sample_transaction_output]

        client = app.test_client(self)
        response = client.post(
            '/transaction',
            json={
                'inputs': [{'transaction_output_id': sample_transaction_output.id}],
                'outputs': [{'address': 'address_recipient', 'amount': 50}]
            })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Invalid transaction')
    def test_the_app_can_create_a_transaction(self):
        AppBlockChain.transaction_output_pool = [sample_transaction_output]

        client = app.test_client(self)
        response = client.post(
            '/transaction',
            json={
                'inputs': [{'transaction_output_id': sample_transaction_output.id}],
                'outputs': [{'address': 'address_recipient', 'amount': 1}]
            })

        self.assertEqual(response.status_code, 201)

    def test_the_app_returns_correct_if_the_chain_is_valid(self):
        client = app.test_client(self)
        response = client.get('/valid')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('valid' in response.json)
        self.assertTrue(response.json['valid'] == AppBlockChain.is_valid())
