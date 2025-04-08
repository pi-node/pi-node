import socket

class QKDClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def request_key(self):
        # Send request to QKD service
        self.socket.send(b'request_key')

        # Receive secure key from QKD service
        secure_key = self.socket.recv(1024)

        return secure_key
