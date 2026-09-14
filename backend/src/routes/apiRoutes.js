// backend/src/routes/apiRoutes.js

const express = require('express');
const router = express.Router();
const apiService = require('../services/apiService');
const Joi = require('joi');

// Define a schema for validating request parameters
const fetchDataSchema = Joi.object({
    endpoint: Joi.string().required(),
});

// Fetch data from the public API
router.get('/data', async (req, res) => {
    const { endpoint } = req.query;

    // Validate query parameters
    const { error } = fetchDataSchema.validate({ endpoint });
    if (error) {
        return res.status(400).json({ success: false, message: error.details[0].message });
    }

    try {
        const data = await apiService.fetchData(endpoint);
        res.status(200).json({ success: true, data });
    } catch (error) {
        console.error('Error fetching data:', error);
        res.status(500).json({ success: false, message: 'Failed to fetch data from the public API' });
    }
});

// Example of another endpoint to demonstrate structure
router.get('/example', (req, res) => {
    res.status(200).json({ success: true, message: 'This is an example endpoint' });
});

// Add more routes as needed...

module.exports = router;
