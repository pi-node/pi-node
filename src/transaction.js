// src/transaction.js
class Transaction {
    constructor(sender, receiver, amount) {
        this.sender = sender;
        this.receiver = receiver;
        this.amount = amount;
        this.timestamp = Date.now();
    }
}

module.exports = Transaction;
