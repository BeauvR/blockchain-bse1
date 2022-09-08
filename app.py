from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify({
        "hash": "0000000000000bae09a7a393a8acded75aa67e46cb81f7acaa5ad94f9eacd103",
        "ver": 1,
        "prev_block": "00000000000007d0f98d9edca880a6c124e25095712df8952e0439ac7409738a",
        "mrkl_root": "935aa0ed2e29a4b81e0c995c39e06995ecce7ddbebb26ed32d550a72e8200bf5",
        "time": 1322131230,
        "bits": 437129626,
        "nonce": 2964215930,
        "n_tx": 22,
        "size": 9195,
        "block_index": 818044,
        "main_chain": True,
        "height": 154595,
        "received_time": 1322131301,
        "relayed_by": "108.60.208.156",
        "tx": [
            "--Array of Transactions--"
        ]
    })


if __name__ == '__main__':
    app.run()
