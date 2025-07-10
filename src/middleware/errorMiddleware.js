// src/middleware/errorMiddleware.js

// Error handling middleware
const errorMiddleware = (err, req, res, next) => {
    console.error(err.stack); // Log the error stack for debugging

    // Send a standardized error response
    res.status(err.status || 500).json({
        error: {
            message: err.message || 'Internal Server Error',
            status: err.status || 500,
        },
    });
};

module.exports = errorMiddleware;
