# Advanced wallet core functionality
import hashlib
import ecdsa

class WalletCore:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = self.generate_public_key(private_key)

    def generate_public_key(self, private_key):
        # Generate public key from private key using ECDSA
        return ecdsa.VerifyingKey.from_string(private_key, curve=ecdsa.SECP256k1).to_string()

    def sign_transaction(self, transaction):
        # Sign transaction using private key
        signature = ecdsa.SigningKey.from_string(self.private_key, curve=ecdsa.SECP256k1).sign(transaction)
        return signature

    def verify_signature(self, transaction, signature):
        # Verify signature using public key
        return ecdsa.VerifyingKey.from_string(self.public_key, curve=ecdsa.SECP256k1).verify(signature, transaction)
