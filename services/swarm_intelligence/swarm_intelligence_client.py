import socket

class SwarmIntelligenceClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def optimize(self, objective_function, bounds):
        # Send request to optimize
        self.socket.send(b"optimize")
        self.socket.send(objective_function)
        self.socket.send(bounds)
        result = self.socket.recv(1024)
        return result

    def solve(self, problem):
        # Send request to solve
        self.socket.send(b"solve")
        self.socket.send(problem)
        solution = self.socket.recv(1024)
        return solution
