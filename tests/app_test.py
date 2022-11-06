from App import app, BlockChain as AppBlockChain

import unittest
from mock import *
import time

from Classes.Block import Block

mock_time = Mock()
mock_time.return_value = 1234567890


class AppTestCase(unittest.TestCase):
    def test_when_the_app_runs_a_genesis_block_is_created(self):
        client = app.test_client(self)
        response = client.get('/genesisBlock')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['previous_hash'] == 0)

    def test_the_app_returns_the_correct_difficulty(self):
        client = app.test_client(self)
        response = client.get('/difficulty')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json == AppBlockChain.difficulty)

    @patch('time.time_ns', mock_time)
    def test_when_the_app_runs_it_returns_the_correct_last_block(self):
        newest_block = Block(['test_transaction1', 'test_transaction2'], 0)
        AppBlockChain.chain.append(newest_block)

        client = app.test_client(self)
        response = client.get('/lastBlock')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['hash'] == newest_block.hash)

    def test_when_the_app_runs_it_returns_the_correct_chain(self):
        # reset the chain for testing
        AppBlockChain.create_genesis_block()
        block = Block(['test_transaction1', 'test_transaction2'], 0)
        AppBlockChain.chain.append(block)

        client = app.test_client(self)
        response = client.get('/chain')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json[0]['previous_hash'] == 0)
        self.assertTrue(response.json[1]['hash'] == block.hash)
    @patch('time.time_ns', mock_time)
    def test_the_app_can_create_a_block_where_the_correct_nonce_is_calculated(self):
        # reset the chain for testing
        AppBlockChain.create_genesis_block()
        block = AppBlockChain.transactions = ['test_transactions']

        client = app.test_client(self)
        response = client.post('/block')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('nonce' in response.json)
        self.assertTrue(response.json['nonce'] == 6)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['hash'] == AppBlockChain.get_last_block().hash)

    def test_the_app_can_get_a_block(self):
        block = Block(['test_transaction1', 'test_transaction2'], 0)
        AppBlockChain.chain.append(block)

        client = app.test_client(self)
        response = client.get('/block/' + block.hash)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['hash'] == block.hash)
        self.assertTrue('transactions' in response.json)
        self.assertTrue(response.json['transactions'] == ['test_transaction1', 'test_transaction2'])

    def test_the_app_returns_404_when_a_block_is_not_found(self):
        client = app.test_client(self)
        response = client.get('/block/invalid_hash')

        self.assertEqual(response.status_code, 404)

    def test_the_app_returns_a_error_when_the_sender_is_more_than_50_characters(self):
        client = app.test_client(self)
        response = client.post('/transaction',
                               json={'sender': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                                     'recipient': 'recipient', 'amount': 50})

        self.assertEqual(response.status_code, 400)

    def test_the_app_returns_a_error_when_the_recipient_is_more_than_50_characters(self):
        client = app.test_client(self)
        response = client.post('/transaction',
                               json={'sender': 'sender',
                                     'recipient': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                                     'amount': 50})

        self.assertEqual(response.status_code, 400)

    def test_the_app_returns_a_error_when_the_transaction_amount_is_not_a_integer(self):
        client = app.test_client(self)
        response = client.post('/transaction', json={'sender': 'sender', 'recipient': 'recipient', 'amount': 'amount'})

        self.assertEqual(response.status_code, 400)

    def test_the_app_returns_a_error_when_the_transaction_amount_is_negative(self):
        client = app.test_client(self)
        response = client.post('/transaction', json={'sender': 'sender', 'recipient': 'recipient', 'amount': -50})

        self.assertEqual(response.status_code, 400)

    def test_the_app_can_create_a_transaction(self):
        client = app.test_client(self)
        response = client.post('/transaction', json={'sender': 'sender', 'recipient': 'recipient', 'amount': 50})

        self.assertEqual(response.status_code, 200)
        self.assertTrue('sender' in response.json)
        self.assertTrue(response.json['sender'] == 'sender')
        self.assertTrue('recipient' in response.json)
        self.assertTrue(response.json['recipient'] == 'recipient')
        self.assertTrue('amount' in response.json)
        self.assertTrue(response.json['amount'] == 50)

    def test_the_app_returns_correct_if_the_chain_is_valid(self):
        client = app.test_client(self)
        response = client.get('/valid')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('valid' in response.json)
        self.assertTrue(response.json['valid'] == AppBlockChain.is_valid())
