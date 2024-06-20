import numpy as np
from qiskit import QuantumCircuit, execute

class QKDService:
    def __init__(self):
        self.quantum_circuit = QuantumCircuit(2, 2)

    def generate_key(self):
        # Generate a quantum key using QKD
        self.quantum_circuit.h(0)
        self.quantum_circuit.cx(0, 1)
        self.quantum_circuit.measure(0, 0)
        self.quantum_circuit.measure(1, 1)
        job = execute(self.quantum_circuit, backend='qasm_simulator')
        result = job.result()
        key = result.get_counts()
        return key

    def encrypt_data(self, data, key):
        # Encrypt data using the quantum key
        encrypted_data = []
        for i, bit in enumerate(data):
            encrypted_data.append(bit ^ key[i % len(key)])
        return encrypted_data

    def decrypt_data(self, encrypted_data, key):
        # Decrypt data using the quantum key
        decrypted_data = []
        for i, bit in enumerate(encrypted_data):
            decrypted_data.append(bit ^ key[i % len(key)])
        return decrypted_data
