import socket

class QMLClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def classify(self, input_data):
        # Send input data to QML service
        self.socket.send(input_data)

        # Receive output data from QML service
        output_data = self.socket.recv(1024)
        return output_data
