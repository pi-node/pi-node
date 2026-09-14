// src/main/index.js

const express = require('express');
const bodyParser = require('body-parser');
const logger = require('./logger');
const shardManager = require('../utils/shardManager');
const transactionRoutes = require('../routes/transactionRoutes');
const shardRoutes = require('../routes/shardRoutes');
const sidechainRoutes = require('../routes/sidechainRoutes');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
app.use(logger);

// Routes
app.use('/api/transactions', transactionRoutes);
app.use('/api/shards', shardRoutes);
app.use('/api/sidechains', sidechainRoutes);

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
