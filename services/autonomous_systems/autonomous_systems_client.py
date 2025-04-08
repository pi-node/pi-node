import socket

class AutonomousSystemsClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def control(self, state, reference):
        # Send request to control
        self.socket.send(b"control")
        self.socket.send(state)
        self.socket.send(reference)
        u = self.socket.recv(1024)
        return u

    def simulate(self, state, u):
        # Send request to simulate
        self.socket.send(b"simulate")
        self.socket.send(state)
        self.socket.send(u)
        next_state = self.socket.recv(1024)
        return next_state
