import unittest

from Classes.block import Block
from Classes.node import Node


class NodeTestCase(unittest.TestCase):

    def test_the_node_can_be_initialized(self):
        node = Node(
            '127.0.0.1',
            5000,
        )

        self.assertIsInstance(node, Node)

    def test_the_node_url_is_correctly_set(self):
        node = Node(
            '127.0.0.1',
            5000,
        )

        self.assertEqual('127.0.0.1:5000', node.url)

    def test_there_can_be_a_block_broadcasted_to_the_node(self):
        node = Node(
            '127.0.0.1',
            5000,
        )

        res = node.broadcast_block(Block([], '0000'))

        self.assertIsNone(res)

    def test_the_node_can_be_converted_to_a_string(self):
        node = Node(
            '127.0.0.1',
            5000,
        )

        self.assertEqual(node.url, str(node))

    def test_the_node_can_be_converted_to_a_dict(self):
        node = Node(
            '127.0.0.1',
            5000,
        )

        self.assertEqual({
            'address': '127.0.0.1',
            'port': 5000,
            'url': '127.0.0.1:5000',
        }, node.__dict__())
