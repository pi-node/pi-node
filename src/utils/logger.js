// src/utils/logger.js

const fs = require('fs');
const path = require('path');

// Define the log file path
const logFilePath = path.join(__dirname, 'app.log');

// Logging utility
const logger = {
    log: (message) => {
        const timestamp = new Date().toISOString();
        const logMessage = `${timestamp} - INFO: ${message}\n`;
        console.log(logMessage); // Log to console
        fs.appendFileSync(logFilePath, logMessage); // Append to log file
    },

    error: (message) => {
        const timestamp = new Date().toISOString();
        const logMessage = `${timestamp} - ERROR: ${message}\n`;
        console.error(logMessage); // Log to console
        fs.appendFileSync(logFilePath, logMessage); // Append to log file
    },

    warn: (message) => {
        const timestamp = new Date().toISOString();
        const logMessage = `${timestamp} - WARN: ${message}\n`;
        console.warn(logMessage); // Log to console
        fs.appendFileSync(logFilePath, logMessage); // Append to log file
    },
};

module.exports = logger;
