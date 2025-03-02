// src/routes/governanceRoutes.js

const express = require('express');
const governanceController = require('../controllers/governanceController');

const router = express.Router();

// Route to create a new governance proposal
router.post('/propose', governanceController.createProposal);

// Route to vote on a governance proposal
router.post('/vote', governanceController.voteOnProposal);

// Export the router
module.exports = router;
