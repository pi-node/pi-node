// Import required packages
const express = require('express');
const stableCoinController = require('./controllers/stableCoinController');
const governanceController = require('./controllers/governanceController');

// Create a new router instance
const router = express.Router();

// StableCoin routes
// Get the balance of a specific account
router.get('/balance/:address', stableCoinController.getBalance);

// Send Pi Coin from one account to another
router.post('/send', stableCoinController.sendPiCoin);

// Governance routes
// Create a new governance proposal
router.post('/propose', governanceController.createProposal);

// Vote on a governance proposal
router.post('/vote', governanceController.voteOnProposal);

// Export the router
module.exports = router;
