// exchangeApi.js
const axios = require("axios");

class ExchangeAPI {
    constructor(apiUrl) {
        this.apiUrl = apiUrl; // Base URL for the exchange API
    }

    async getExchangeRate() {
        try {
            const response = await axios.get(`${this.apiUrl}/exchange-rate`);
            return response.data.rate; // Assuming the response contains a 'rate' field
        } catch (error) {
            console.error("Error fetching exchange rate:", error.message);
            throw error;
        }
    }

    async convertToStableValue(amount) {
        const rate = await this.getExchangeRate();
        return amount * rate; // Convert to stable value based on the exchange rate
    }
}

module.exports = ExchangeAPI;
