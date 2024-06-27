# node_communication.py
import socket

class NodeCommunication:
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        self.socket.connect((self.host, self.port))

    def send_command(self, command: str) -> None:
        self.socket.sendall(command.encode())

    def receive_response(self) -> str:
        response = self.socket.recv(1024)
        return response.decode()

    def close(self) -> None:
        self.socket.close()
