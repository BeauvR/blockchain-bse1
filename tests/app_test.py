from app import app

import unittest


class AppTestCase(unittest.TestCase):
    def test_the_endpoint_returns_the_correct_status(self):
        response = self.makeIndexRequest()
        self.assertEqual(response.status_code, 200)

    def test_the_endpoint_returns_the_correct_headers(self):
        response = self.makeIndexRequest()
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_the_endpoint_returns_returns_json_with_the_correct_structure(self):
        response = self.makeIndexRequest()
        self.assertTrue('hash' in response.json)
        self.assertTrue('ver' in response.json)
        self.assertTrue('prev_block' in response.json)
        self.assertTrue('mrkl_root' in response.json)
        self.assertTrue('time' in response.json)
        self.assertTrue('bits' in response.json)
        self.assertTrue('nonce' in response.json)
        self.assertTrue('n_tx' in response.json)
        self.assertTrue('size' in response.json)
        self.assertTrue('block_index' in response.json)
        self.assertTrue('main_chain' in response.json)
        self.assertTrue('height' in response.json)
        self.assertTrue('received_time' in response.json)
        self.assertTrue('relayed_by' in response.json)
        self.assertTrue('tx' in response.json)
        self.assertTrue('--Array of Transactions--' in response.json['tx'])

    def makeIndexRequest(self):
        tester = app.test_client(self)
        return tester.get('/', content_type='application/json')


if __name__ == '__main__':
    unittest.main()
