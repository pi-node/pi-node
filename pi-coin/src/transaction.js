// src/transaction.js
const crypto = require('crypto');
const PI_COIN = require('./constant');

class Transaction {
    constructor(sender, receiver, amount) {
        this.sender = sender;
        this.receiver = receiver;
        this.amount = amount;
        this.timestamp = Date.now();
        this.transactionId = this.generateTransactionId();
    }

    // Generate a unique transaction ID
    generateTransactionId() {
        return crypto.randomBytes(16).toString('hex');
    }

    // Validate the transaction
    validate() {
        if (!this.sender || !this.receiver || !this.amount) {
            throw new Error("Transaction must include sender, receiver, and amount.");
        }
        if (this.amount <= 0) {
            throw new Error("Transaction amount must be greater than zero.");
        }
        // Additional validation can be added here (e.g., checking sender's balance)
    }

    // Log the transaction details
    logTransaction() {
        console.log(`Transaction ID: ${this.transactionId}`);
        console.log(`Sender: ${this.sender}`);
        console.log(`Receiver: ${this.receiver}`);
        console.log(`Amount: ${this.amount}`);
        console.log(`Timestamp: ${new Date(this.timestamp).toISOString()}`);
    }
}

// Example usage
function createTransaction(sender, receiver, amount) {
    const transaction = new Transaction(sender, receiver, amount);
    transaction.validate(); // Validate the transaction
    transaction.logTransaction(); // Log the transaction details
    return transaction; // Return the created transaction
}

module.exports = {
    Transaction,
    createTransaction,
};
