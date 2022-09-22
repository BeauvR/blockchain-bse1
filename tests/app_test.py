from App import app, BlockChain as AppBlockChain

import unittest


class AppTestCase(unittest.TestCase):
    def test_when_the_app_runs_a_genesis_block_is_created(self):
        client = app.test_client(self)
        response = client.get('/genesisBlock')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['previous_hash'] == 0)

    def test_when_the_app_runs_it_returns_the_correct_last_block(self):
        newest_block = AppBlockChain.add_block(['test_transactions'])

        client = app.test_client(self)
        response = client.get('/lastBlock')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['hash'] == newest_block.hash)

    def test_when_the_app_runs_it_returns_the_correct_chain(self):
        # reset the chain for testing
        AppBlockChain.create_genesis_block()
        block = AppBlockChain.add_block(['test_transactions'])

        client = app.test_client(self)
        response = client.get('/chain')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json[0]['previous_hash'] == 0)
        self.assertTrue(response.json[1]['hash'] == block.hash)

    def test_the_app_can_create_a_block(self):
        client = app.test_client(self)
        response = client.post('/block', json={'transactions': ['test transactions']})

        self.assertEqual(response.status_code, 200)
        self.assertTrue('hash' in response.json)
        self.assertTrue(response.json['hash'] == AppBlockChain.get_last_block().hash)
        self.assertTrue('transactions' in response.json)
        self.assertTrue(response.json['transactions'] == ['test transactions'])

    def test_the_app_validate_the_request_before_creating_a_block(self):
        client = app.test_client(self)
        response = client.post('/block', json={})

        self.assertEqual(response.status_code, 400)

    def test_the_app_can_get_a_block(self):
        block = AppBlockChain.add_block(['test_transaction1', 'test_transaction2'])

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
