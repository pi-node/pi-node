// src/routes/transactionRoutes.js

const express = require('express');
const router = express.Router();
const shardManager = require('../utils/shardManager');
const consensus = require('../utils/consensus');
const encryption = require('../utils/encryption');

// Sample transaction data
let transactions = [];

// Create a new transaction
router.post('/', async (req, res) => {
    const { sourceSecret, operations, encryptData } = req.body;

    try {
        // Encrypt transaction data if specified
        const transactionData = encryptData ? encryption.encrypt(req.body) : req.body;

        // Create a transaction using the consensus utility
        const transaction = await consensus.createTransaction(sourceSecret, operations);
        
        // Assign a unique ID to the transaction
        transaction.id = transactions.length;
        transactions.push(transactionData); // Store the transaction data

        // Add transaction data to the appropriate shard
        const shardIndex = shardManager.addData(transactionData);

        res.status(201).json({ message: 'Transaction created', transactionId: transaction.id, shardIndex });
    } catch (error) {
        console.error('Error creating transaction:', error);
        res.status(500).json({ success: false, message: error.message });
    }
});

// Get all transactions
router.get('/', (req, res) => {
    res.json(transactions);
});

// Get a specific transaction by ID
router.get('/:id', (req, res) => {
    const transactionId = parseInt(req.params.id);
    const transaction = transactions.find(tx => tx.id === transactionId);

    if (transaction) {
        res.json(transaction);
    } else {
        res.status(404).json({ success: false, message: 'Transaction not found' });
    }
});

// Delete a transaction by ID
router.delete('/:id', (req, res) => {
    const transactionId = parseInt(req.params.id);
    const transactionIndex = transactions.findIndex(tx => tx.id === transactionId);

    if (transactionIndex !== -1) {
        transactions.splice(transactionIndex, 1);
        res.status(200).json({ success: true, message: 'Transaction deleted' });
    } else {
        res.status(404).json({ success: false, message: 'Transaction not found' });
    }
});

// Validate a transaction
router.post('/validate', async (req, res) => {
    const { transactionId } = req.body;

    try {
        const transaction = transactions.find(tx => tx.id === transactionId);
        if (!transaction) {
            return res.status(404).json({ success: false, message: 'Transaction not found' });
        }

        // Validate the transaction using the consensus utility
        const status = await consensus.getTransactionStatus(transactionId);
        res.status(200).json({ success: true, status });
    } catch (error) {
        console.error('Error validating transaction:', error);
        res.status(500).json({ success: false, message: error.message });
    }
});

module.exports = router;
