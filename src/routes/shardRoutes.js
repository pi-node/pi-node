// src/routes/shardRoutes.js

const express = require('express');
const router = express.Router();
const shardManager = require('../utils/shardManager');

// Get data from a specific shard
router.get('/:shardIndex', (req, res) => {
    const shardIndex = parseInt(req.params.shardIndex);
    const shardData = shardManager.getShardData(shardIndex);
    if (shardData) {
        res.json(shardData);
    } else {
        res.status(404).json({ message: 'Shard not found' });
    }
});

// Get all shards
router.get('/', (req, res) => {
    const allShards = shardManager.getAllShards();
    res.json(allShards);
});

module.exports = router;
