# Advanced transaction management functionality
import hashlib
from cryptography.hazmat.primitives import hashes

class TransactionManager:
    def __init__(self, wallet_core):
        self.wallet_core = wallet_core

    def create_transaction(self, sender, recipient, amount):
        # Create a new transaction
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': int(time.time())
        }
        transaction_hash = hashlib.sha256(json.dumps(transaction).encode()).hexdigest()
        return transaction, transaction_hash

    def sign_transaction(self, transaction):
        # Sign transaction using wallet core
        signature = self.wallet_core.sign_transaction(transaction)
        return signature

    def verify_transaction(self, transaction, signature):
        # Verify transaction using wallet core
        return self.wallet_core.verify_signature(transaction, signature)

    def encrypt_transaction(self, transaction):
        # Encrypt transaction using wallet core
        encrypted_transaction = self.wallet_core.encrypt_data(json.dumps(transaction).encode())
        return encrypted_transaction

    def decrypt_transaction(self, encrypted_transaction):
        # Decrypt transaction using wallet core
        decrypted_transaction = self.wallet_core.decrypt_data(encrypted_transaction)
        return json.loads(decrypted_transaction.decode())
