# Advanced blockchain management functionality
import hashlib

class BlockchainManager:
    def __init__(self, transaction_manager):
        self.transaction_manager = transaction_manager
        self.blockchain = []

    def create_block(self, transactions):
        # Create a new block
        block = {
            'transactions': transactions,
            'previous_block_hash': self.get_previous_block_hash(),
            'timestamp': int(time.time())
        }
        block_hash = hashlib.sha256(json.dumps(block).encode()).hexdigest()
        return block, block_hash

    def add_block(self, block):
        # Add block to blockchain
        self.blockchain.append(block)

    def get_previous_block_hash(self):
        # Get previous block hash
        if not self.blockchain:
            return '0' * 64
        return self.blockchain[-1]['block_hash']
