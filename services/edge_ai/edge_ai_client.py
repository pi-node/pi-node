import socket

class EdgeAIClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def train(self, X, y):
        # Send request to train
        self.socket.send(b"train")
        self.socket.send(X)
        self.socket.send(y)
        response = self.socket.recv(1024)
        return response

    def predict(self, X):
        # Send request to predict
        self.socket.send(b"predict")
        self.socket.send(X)
        response = self.socket.recv(1024)
        return response
