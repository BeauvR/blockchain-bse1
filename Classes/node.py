class Node(object):
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        self.url = self.address + ":" + str(self.port)

    def __str__(self) -> str:
        return str(self.url)

    def __dict__(self) -> dict:
        return {
            "address": self.address,
            "port": self.port,
            "url": self.url
        }