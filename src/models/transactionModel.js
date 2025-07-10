// src/models/transactionModel.js

class Transaction {
    constructor(id, from, to, amount, assetCode, transactionHash) {
        this.id = id; // Unique identifier for the transaction
        this.from = from; // Sender's Stellar address
        this.to = to; // Recipient's Stellar address
        this.amount = amount; // Amount of the asset being transferred
        this.assetCode = assetCode; // Asset code (e.g., PiCoin)
        this.transactionHash = transactionHash; // Transaction hash from Stellar
        this.createdAt = new Date(); // Timestamp of when the transaction was created
    }
}

// Example in-memory transaction storage (for demonstration purposes)
const transactions = [];

// Function to create a new transaction
const createTransaction = (from, to, amount, assetCode, transactionHash) => {
    const id = transactions.length + 1; // Simple ID generation
    const newTransaction = new Transaction(id, from, to, amount, assetCode, transactionHash);
    transactions.push(newTransaction);
    return newTransaction;
};

// Function to find a transaction by ID
const findTransactionById = (id) => {
    return transactions.find(transaction => transaction.id === id);
};

// Export the Transaction model and functions
module.exports = {
    Transaction,
    createTransaction,
    findTransactionById,
};
