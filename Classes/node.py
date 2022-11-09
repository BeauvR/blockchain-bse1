import json
from urllib import request


class Node(object):
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        self.url = self.address + ":" + str(self.port)

    def broadcast_block(self, block):
        endpoint = 'http://' + self.url + '/node/block'
        data = json.dumps(block.__dict__())
        data = data.encode('utf-8')
        req = request.Request(endpoint, data=data, method='POST')
        try:
            request.urlopen(req)
        except Exception as e:
            print(e)

    def __str__(self) -> str:
        return str(self.url)

    def __dict__(self) -> dict:
        return {
            "address": self.address,
            "port": self.port,
            "url": self.url
        }
