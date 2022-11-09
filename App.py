from flask import Flask, jsonify, request, Response
from flask_expects_json import expects_json

from Classes.block_chain import BlockChain
from Classes.transaction import Transaction
from Classes.transaction_input import TransactionInput
from Classes.transaction_output import TransactionOutput

block_chain = BlockChain()

app = Flask(__name__)


@app.route('/difficulty', methods=['GET'])
def get_difficulty() -> Response:
    return jsonify(block_chain.difficulty)


@app.route('/genesisBlock', methods=['GET'])
def get_genesis_block() -> Response:
    genesis_block = block_chain.get_genesis_block()
    return jsonify(genesis_block.__dict__())


@app.route('/lastBlock', methods=['GET'])
def get_last_block() -> Response:
    return jsonify(block_chain.get_last_block().__dict__())


@app.route('/chain', methods=['GET'])
def get_chain() -> Response:
    chain = map(lambda block: block.__dict__(), block_chain.chain)
    return jsonify(list(chain))


@app.route('/block', methods=['POST'])
def create_block() -> Response:
    block = block_chain.add_block()

    return jsonify(block.__dict__())


@app.route('/block/<block_hash>', methods=['GET'])
def get_block(block_hash) -> Response:
    block = block_chain.get_block(block_hash)
    if block is None:
        return jsonify({'error': 'Block not found'}), 404
    return jsonify(block.__dict__())


@app.route('/transaction', methods=['POST'])
@expects_json({
    "type": "object",
    "required": ["inputs", "outputs"],
    "properties": {
        "inputs": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["transaction_output_id"],
                "properties": {
                    "transaction_output_id": {"type": "string"}
                },
            }
        },
        "outputs": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["address", "amount"],
                "properties": {
                    "address": {"type": "string"},
                    "amount": {"type": "integer"}
                }
            }
        }
    },
})
def create_transaction():
    transaction_inputs = []
    for requestInput in request.json['inputs']:
        output = block_chain.get_transaction_output(requestInput['transaction_output_id'])
        if output is None:
            return jsonify({'error': 'Invalid transaction output id'}), 400
        transaction_inputs.append(TransactionInput(output))

    transaction_outputs = []
    for requestOutput in request.json['outputs']:
        transaction_outputs.append(TransactionOutput(requestOutput['address'], requestOutput['amount']))

    transaction = Transaction(transaction_inputs, transaction_outputs)

    if not transaction.is_valid(block_chain):
        return jsonify({'error': 'Invalid transaction'}), 400

    block_chain.add_transaction(transaction)

    return jsonify(transaction.__dict__()), 201


@app.route('/valid', methods=['GET'])
def is_valid():
    return jsonify({
        'valid': block_chain.is_valid(),
    })


@app.route('/balance/<address>', methods=['GET'])
def get_balance(address) -> Response:
    balance = block_chain.get_balance(address)
    return jsonify({
        'balance': balance,
    })
