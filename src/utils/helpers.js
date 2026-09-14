// src/utils/helpers.js

// Function to validate Stellar address
const isValidStellarAddress = (address) => {
    return address && address.length === 56; // Basic validation for Stellar addresses
};

// Function to format currency
const formatCurrency = (amount) => {
    return parseFloat(amount).toFixed(2); // Format to two decimal places
};

// Function to generate a random ID
const generateRandomId = () => {
    return Math.random().toString(36).substring(2, 15); // Generate a random string ID
};

// Export utility functions
module.exports = {
    isValidStellarAddress,
    formatCurrency,
    generateRandomId,
};
