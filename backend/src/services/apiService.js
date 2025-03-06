// backend/src/services/apiService.js

const axios = require('axios');
const config = require('../main/config');
const NodeCache = require('node-cache');
const { logger } = require('../main/logger'); // Import the logger

// Create a cache instance with a default TTL of 10 minutes
const cache = new NodeCache({ stdTTL: 600 });

class ApiService {
    // Fetch data from the public API with optional caching
    async fetchData(endpoint) {
        const cacheKey = endpoint; // Use the endpoint as the cache key

        // Check if the data is already cached
        const cachedData = cache.get(cacheKey);
        if (cachedData) {
            logger.info(`Cache hit for endpoint: ${endpoint}`);
            return cachedData; // Return cached data
        }

        try {
            logger.info(`Fetching data from public API for endpoint: ${endpoint}`);
            const response = await axios.get(`${config.PUBLIC_API_URL}/${endpoint}`);
            const data = response.data;

            // Cache the fetched data
            cache.set(cacheKey, data);
            logger.info(`Data fetched and cached for endpoint: ${endpoint}`);

            return data;
        } catch (error) {
            logger.error('Error fetching data from public API:', error);
            throw new Error('Failed to fetch data from public API');
        }
    }
}

module.exports = new ApiService();
