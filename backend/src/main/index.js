// backend/src/main/index.js

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const logger = require('./logger');
const apiRoutes = require('../routes/apiRoutes');
const config = require('./config');

const app = express();
const PORT = config.PORT || 3000;

// Middleware
app.use(cors()); // Enable CORS for all routes
app.use(bodyParser.json()); // Parse JSON request bodies
app.use(logger); // Custom logger middleware

// Health check route
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'OK', message: 'API is running smoothly' });
});

// API routes
app.use('/api', apiRoutes);

// Global error handler
app.use((err, req, res, next) => {
    console.error('Global Error Handler:', err);
    res.status(err.status || 500).json({
        success: false,
        message: err.message || 'Internal Server Error',
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Backend server is running on http://localhost:${PORT}`);
});
