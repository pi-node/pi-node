# homomorphic_encryption_data_processing.py
import helib

class SecureDataProcessor:
    def __init__(self):
        self.context = helib.Context()

    def encrypt(self, data):
        # Encrypt the data using homomorphic encryption
        encrypted_data = self.context.encrypt(data)
        return encrypted_data

    def process_data(self, encrypted_data):
        # Process the encrypted data using homomorphic encryption
        processed_data = self.context.eval(encrypted_data, 'x^2 + 2*x + 1')
        return processed_data

    def decrypt(self, processed_data):
        # Decrypt the processed data using homomorphic encryption
        decrypted_data = self.context.decrypt(processed_data)
        return decrypted_data

# Example usage:
secure_data_processor = SecureDataProcessor()
data = 10
encrypted_data = secure_data_processor.encrypt(data)
processed_data = secure_data_processor.process_data(encrypted_data)
decrypted_data = secure_data_processor.decrypt(processed_data)
print(f"Decrypted data: {decrypted_data}")
