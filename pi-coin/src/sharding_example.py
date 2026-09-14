# Constants
NUM_SHARDS = 4  # Define the number of shards

# Function to shard data based on transactions
def shard_data(transactions):
    shards = {}
    
    # Initialize shards
    for i in range(NUM_SHARDS):
        shards[i] = {
            "transactions": [],
            "transaction_count": 0  # Metadata to track the number of transactions
        }

    # Distribute transactions into shards
    for tx in transactions:
        shard_key = hash(tx.sender) % NUM_SHARDS
        
        # Error handling for invalid shard key
        if shard_key < 0 or shard_key >= NUM_SHARDS:
            raise ValueError("Invalid shard key calculated")
        
        # Add transaction to the appropriate shard
        shards[shard_key]["transactions"].append(tx)
        shards[shard_key]["transaction_count"] += 1  # Update transaction count

    return shards

# Function to retrieve transactions from a specific shard
def get_transactions_from_shard(shards, shard_key):
    if shard_key not in shards:
        raise ValueError("Shard key does not exist")
    return shards[shard_key]["transactions"]

# Example usage
transactions = [
    Transaction(sender="Alice", amount=100),
    Transaction(sender="Bob", amount=200),
    Transaction(sender="Charlie", amount=150),
    Transaction(sender="Alice", amount=50)
]

sharded_data = shard_data(transactions)
print(sharded_data)

# Retrieve transactions from a specific shard
shard_key = 0
transactions_from_shard = get_transactions_from_shard(sharded_data, shard_key)
print(transactions_from_shard)
