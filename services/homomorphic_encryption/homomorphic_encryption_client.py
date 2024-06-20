import socket

class HomomorphicEncryptionClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def encrypt(self, plaintext):
        # Send plaintext to homomorphic encryption service
        self.socket.send(plaintext)

        # Receive encrypted ciphertext from homomorphic encryption service
        ciphertext = self.socket.recv(1024)

        return ciphertext

    def evaluate(self, ciphertext1, ciphertext2):
        # Send ciphertexts to homomorphic encryption service
        self.socket.send(ciphertext1 + b' ' ciphertext2)

        # Receive evaluated ciphertext from homomorphic encryption service
        evaluated_ciphertext = self.socket.recv(1024)

        return evaluated_ciphertext
