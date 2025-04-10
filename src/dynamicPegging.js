// Import necessary libraries
const axios = require('axios');
const { mintTokens, burnTokens, getCurrentSupply } = require('./supplyManager');
const { getPriceFromOracle } = require('./oracleIntegration');
const winston = require('winston'); // For logging

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'dynamicPegging.log' })
    ]
});

// Configuration Constants
const CONFIG = {
    TARGET_PRICE: 314159.00, // Target price in USD
    SUPPLY_ADJUSTMENT_THRESHOLD: 0.01, // 1% threshold for supply adjustment
    ORACLE_URL: 'https://api.chainlink.com/v1/prices/pi-coin', // Example oracle URL
    ADJUSTMENT_FACTOR: 0.1, // Base factor for supply adjustment
    MAX_ADJUSTMENT: 1000000 // Maximum tokens to mint/burn in one adjustment
};

// Function to monitor the price and adjust supply
async function monitorPriceAndAdjustSupply() {
    try {
        // Get the current price of Pi Coin from the oracle
        const currentPrice = await getPriceFromOracle(CONFIG.ORACLE_URL);
        logger.info(`Current Price of Pi Coin: $${currentPrice}`);

        // Calculate the price deviation
        const priceDeviation = ((currentPrice - CONFIG.TARGET_PRICE) / CONFIG.TARGET_PRICE);

        // Check if the deviation exceeds the threshold
        if (Math.abs(priceDeviation) > CONFIG.SUPPLY_ADJUSTMENT_THRESHOLD) {
            logger.info(`Price deviation detected: ${priceDeviation * 100}%`);

            // Adjust supply based on price deviation
            const supplyAdjustment = calculateSupplyAdjustment(priceDeviation);
            if (priceDeviation > 0) {
                // Price is above target, burn tokens
                await burnTokens(supplyAdjustment);
                logger.info(`Burned ${supplyAdjustment} Pi Coins to stabilize price.`);
            } else {
                // Price is below target, mint tokens
                await mintTokens(supplyAdjustment);
                logger.info(`Minted ${supplyAdjustment} Pi Coins to stabilize price.`);
            }
        } else {
            logger.info('No significant price deviation detected. No action taken.');
        }
    } catch (error) {
        logger.error('Error monitoring price and adjusting supply:', error);
    }
}

// Function to calculate the amount of supply to adjust
function calculateSupplyAdjustment(priceDeviation) {
    const currentSupply = getCurrentSupply(); // Get the current supply
    const adjustmentAmount = Math.floor(currentSupply * CONFIG.ADJUSTMENT_FACTOR * Math.abs(priceDeviation));
    return Math.min(adjustmentAmount, CONFIG.MAX_ADJUSTMENT); // Ensure we do not exceed max adjustment
}

// Set an interval to monitor the price every minute
setInterval(monitorPriceAndAdjustSupply, 60000);

// Export the function for external use
module.exports = {
    monitorPriceAndAdjustSupply,
};
