// src/routes/transactionRoutes.js

const express = require('express');
const router = express.Router();
const shardManager = require('../utils/shardManager');

// Sample transaction data
let transactions = [];

// Create a new transaction
router.post('/', (req, res) => {
    const transaction = req.body;
    transaction.id = transactions.length; // Simple ID assignment
    transactions.push(transaction);
    const shardIndex = shardManager.addData(transaction);
    res.status(201).json({ message: 'Transaction created', shardIndex });
});

// Get all transactions
router.get('/', (req, res) => {
    res.json(transactions);
});

module.exports = router;
