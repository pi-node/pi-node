// backend/src/main/logger.js

const winston = require('winston');
const path = require('path');

// Create a logger instance
const logger = winston.createLogger({
    level: 'info', // Default logging level
    format: winston.format.combine(
        winston.format.timestamp(), // Add timestamp to logs
        winston.format.printf(({ timestamp, level, message }) => {
            return `${timestamp} [${level.toUpperCase()}]: ${message}`;
        })
    ),
    transports: [
        // Log to console
        new winston.transports.Console({
            format: winston.format.colorize(), // Colorize console output
        }),
        // Log to a file
        new winston.transports.File({
            filename: path.join(__dirname, 'logs', 'app.log'), // Log file path
            level: 'info', // Log level for file
            format: winston.format.json(), // Log format for file
        }),
    ],
});

// Middleware for logging requests
const requestLogger = (req, res, next) => {
    logger.info(`Incoming request: ${req.method} ${req.url}`);
    next();
};

// Middleware for logging errors
const errorLogger = (err, req, res, next) => {
    logger.error(`Error occurred: ${err.message}`);
    next(err); // Pass the error to the next middleware
};

// Export the logger and middleware
module.exports = {
    logger,
    requestLogger,
    errorLogger,
};
