const express = require('express');
const axios = require('axios'); // For making HTTP requests
const app = express();
const port = 3000;

// Function to fetch exchange rates
async function fetchExchangeRate(from, to) {
    try {
        const response = await axios.get(`https://api.exchangerate-api.com/v4/latest/${from}`);
        const rates = response.data.rates;
        if (rates[to]) {
            return rates[to];
        } else {
            throw new Error(`Currency ${to} not found`);
        }
    } catch (error) {
        throw new Error(`Error fetching exchange rate: ${error.message}`);
    }
}

// API endpoint for currency conversion
app.get('/api/convert', async (req, res) => {
    const { amount, from, to } = req.query;

    // Input validation
    if (!amount || isNaN(amount) || amount <= 0) {
        return res.status(400).json({ error: 'Invalid amount provided' });
    }
    if (!from || !to) {
        return res.status(400).json({ error: 'Both "from" and "to" currencies must be provided' });
    }

    try {
        // Fetch the exchange rate
        const exchangeRate = await fetchExchangeRate(from.toUpperCase(), to.toUpperCase());
        const convertedAmount = (amount * exchangeRate).toFixed(2); // Convert and format to 2 decimal places

        // Send the response
        res.json({ convertedAmount, from, to });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`API listening at http://localhost:${port}`);
});
