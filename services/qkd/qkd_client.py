import socket

class QKDClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def generate_key(self):
        # Send request to generate a quantum key
        self.socket.send(b"generate_key")
        key = self.socket.recv(1024)
        return key

    def encrypt_data(self, data, key):
        # Send request to encrypt data
        self.socket.send(b"encrypt_data")
        self.socket.send(data)
        self.socket.send(key)
        encrypted_data = self.socket.recv(1024)
        return encrypted_data

    def decrypt_data(self, encrypted_data, key):
        # Send request to decrypt data
        self.socket.send(b"decrypt_data")
        self.socket.send(encrypted_data)
        self.socket.send(key)
        decrypted_data = self.socket.recv(1024)
        return decrypted_data
