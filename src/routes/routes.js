// Import required packages
const express = require('express');
const stableCoinController = require('./controllers/stableCoinController');
const governanceController = require('./controllers/governanceController');
const { body, param, validationResult } = require('express-validator');

// Create a new router instance
const router = express.Router();

// Middleware for validation
const validateAddress = param('address').isString().isLength({ min: 1 }).withMessage('Address must be a valid string.');
const validateSend = [
    body('senderSecret').isString().withMessage('Sender secret is required.'),
    body('receiverPublicKey').isString().isLength({ min: 1 }).withMessage('Receiver public key is required.'),
    body('amount').isNumeric().withMessage('Amount must be a number and greater than 0.').custom(value => {
        if (value <= 0) {
            throw new Error('Amount must be greater than 0.');
        }
        return true;
    })
];

// StableCoin routes
// Get the balance of a specific account
router.get('/balance/:address', validateAddress, async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
    }
    try {
        const balance = await stableCoinController.getBalance(req.params.address);
        res.status(200).json({ success: true, balance });
    } catch (error) {
        console.error("Error fetching balance:", error);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Send Pi Coin from one account to another
router.post('/send', validateSend, async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
    }
    try {
        const result = await stableCoinController.sendPiCoin(req.body.senderSecret, req.body.receiverPublicKey, req.body.amount);
        res.status(200).json({ success: true, result });
    } catch (error) {
        console.error("Error sending Pi Coin:", error);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Governance routes
// Create a new governance proposal
router.post('/propose', async (req, res) => {
    try {
        const proposal = await governanceController.createProposal(req.body);
        res.status(201).json({ success: true, proposal });
    } catch (error) {
        console.error("Error creating proposal:", error);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Vote on a governance proposal
router.post('/vote', async (req, res) => {
    try {
        const result = await governanceController.voteOnProposal(req.body);
        res.status(200).json({ success: true, result });
    } catch (error) {
        console.error("Error voting on proposal:", error);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Export the router
module.exports = router;
