const express = require('express');
const app = express();
const port = 3000;

// Mock function to simulate database access
async function getMetricsFromDatabase() {
    // Simulate a database call
    return [
        { id: 1, metricName: "Active Users", value: 1500 },
        { id: 2, metricName: "Page Views", value: 3000 },
        { id: 3, metricName: "Conversion Rate", value: 2.5 }
    ];
}

// Middleware for logging requests
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    next();
});

// API endpoint for fetching metrics
app.get('/api/metrics', async (req, res) => {
    try {
        const metrics = await getMetricsFromDatabase(); // Fetch data from the database
        res.status(200).json({
            success: true,
            data: metrics,
            message: "Metrics retrieved successfully"
        });
    } catch (error) {
        console.error("Error fetching metrics:", error);
        res.status(500).json({
            success: false,
            message: "Error fetching metrics",
            error: error.message
        });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`API listening at http://localhost:${port}`);
});
