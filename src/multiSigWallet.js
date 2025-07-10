// multiSigWallet.js
const { ethers } = require('ethers');

class MultiSigWallet {
    constructor(signers, requiredSignatures) {
        this.signers = signers; // Array of signers' addresses
        this.requiredSignatures = requiredSignatures; // Number of required signatures
        this.transactions = []; // List of transactions
    }

    createTransaction(to, value) {
        const transaction = {
            to,
            value,
            confirmations: [],
        };
        this.transactions.push(transaction);
        return transaction;
    }

    confirmTransaction(transactionIndex, signer) {
        const transaction = this.transactions[transactionIndex];
        if (!transaction) {
            throw new Error('Transaction not found.');
        }
        if (transaction.confirmations.includes(signer)) {
            throw new Error('Transaction already confirmed by this signer.');
        }
        transaction.confirmations.push(signer);
        if (transaction.confirmations.length >= this.requiredSignatures) {
            this.executeTransaction(transaction);
        }
    }

    executeTransaction(transaction) {
        // Logic to execute the transaction (e.g., transfer funds)
        console.log(`Executing transaction to ${transaction.to} for ${transaction.value} units.`);
        // Reset confirmations after execution
        transaction.confirmations = [];
    }
}

module.exports = MultiSigWallet;
