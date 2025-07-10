// src/routes/stableCoinRoutes.js

const express = require('express');
const stableCoinController = require('../controllers/stableCoinController');

const router = express.Router();

// Route to get the balance of a specific account
router.get('/balance/:address', stableCoinController.getBalance);

// Route to send Pi Coin from one account to another
router.post('/send', stableCoinController.sendPiCoin);

// Export the router
module.exports = router;
