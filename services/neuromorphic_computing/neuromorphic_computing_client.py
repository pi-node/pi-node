import socket

class NeuromorphicComputingClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def process_data(self, data):
        # Send request to process data
        self.socket.send(b"process_data")
        self.socket.send(data)
        output = self.socket.recv(1024)
        return output

    def learn(self, data, labels):
        # Send request to learn
        self.socket.send(b"learn")
        self.socket.send(data)
        self.socket.send(labels)
