from flask import Flask, jsonify, request
from flask_expects_json import expects_json

from Classes.BlockChain import BlockChain

BlockChain = BlockChain()

app = Flask(__name__)


@app.route('/genesisBlock', methods=['GET'])
def get_genesis_block():
    return jsonify(BlockChain.get_genesis_block().__dict__)


@app.route('/lastBlock', methods=['GET'])
def get_last_block():
    return jsonify(BlockChain.get_last_block().__dict__)


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = map(lambda block: block.__dict__, BlockChain.chain)
    return jsonify(list(chain))


@app.route('/block', methods=['POST'])
@expects_json({
    'type': 'object',
    'properties': {
        'transactions': {
            'type': 'array',
        },
    },
    'required': ['transactions'],
})
def create_block():
    block = BlockChain.add_block(request.json['transactions'])
    return jsonify(block.__dict__)


@app.route('/block/<block_hash>', methods=['GET'])
def get_block(block_hash):
    block = BlockChain.get_block(block_hash)
    if block is None:
        return jsonify({'error': 'Block not found'}), 404
    return jsonify(block.__dict__)


@app.route('/transaction', methods=['POST'])
@expects_json({
    'type': 'object',
    'properties': {
        'sender': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 50,
            'pattern': '^[a-zA-Z0-9]+$',
        },
        'recipient': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 50,
            'pattern': '^[a-zA-Z0-9]+$',
        },
        'amount': {
            'type': 'integer',
            'minimum': 1,
        },
    },
})
def create_transaction():
    transaction = BlockChain.add_transaction(
        request.json['sender'],
        request.json['recipient'],
        request.json['amount'],
    )
    return jsonify(transaction.__dict__)
