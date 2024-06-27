# encrypted_communication.py
import os
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Node:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            algorithm=rsa.RSA(),
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, message, recipient_public_key):
        # Encrypt the message using the recipient's public key
        encrypted_message = recipient_public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_message)

    def decrypt(self, encrypted_message):
        # Decrypt the message using the node's private key
        decrypted_message = self.private_key.decrypt(
            base64.b64decode(encrypted_message),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode()

# Example usage:
node1 = Node()
node2 = Node()

message = "Hello, secure world!"
encrypted_message = node1.encrypt(message.encode(), node2.public_key)
print(f"Encrypted message: {encrypted_message}")

decrypted_message = node2.decrypt(encrypted_message)
print(f"Decrypted message: {decrypted_message}")
