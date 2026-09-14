// src/routes/sidechainRoutes.js

const express = require('express');
const router = express.Router();

// Placeholder for sidechain logic
let sidechains = {};

// Create a new sidechain
router.post('/', (req, res) => {
    const { name } = req.body;
    if (!name) {
        return res.status(400).json({ message: 'Sidechain name is required' });
    }
    sidechains[name] = [];
    res.status(201).json({ message: 'Sidechain created', name });
});

// Get all sidechains
router.get('/', (req, res) => {
    res.json(sidechains);
});

module.exports = router;
