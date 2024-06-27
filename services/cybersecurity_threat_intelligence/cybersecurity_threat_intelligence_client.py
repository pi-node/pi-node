import socket

class CybersecurityThreatIntelligenceClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def predict_threat(self, description):
        # Sendrequest to predict threat
        self.socket.send(b"predict_threat")
        self.socket.send(description.encode())
        y_pred = self.socket.recv(1024)
        return y_pred

    def analyze_threat(self, description):
        # Send request to analyze threat
        self.socket.send(b"analyze_threat")
        self.socket.send(description.encode())
        entities = self.socket.recv(1024)
        return entities
