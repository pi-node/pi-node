// Quantum-specific configuration file

const quantumConfig = {
    // Quantum service configuration
    service: {
        endpoint: process.env.QUANTUM_SERVICE_URL || 'http://localhost:5000', // Default to local quantum service
        apiKey: process.env.QUANTUM_API_KEY || 'your-api-key-here', // Replace with your actual API key
    },

    // Quantum algorithm settings
    algorithms: {
        piEstimation: {
            iterations: process.env.PI_ESTIMATION_ITERATIONS || 1000, // Number of iterations for Pi estimation
            precision: process.env.PI_ESTIMATION_PRECISION || 10, // Precision for the estimation
        },
        optimization: {
            maxIterations: process.env.OPTIMIZATION_MAX_ITERATIONS || 500, // Maximum iterations for optimization algorithms
            tolerance: process.env.OPTIMIZATION_TOLERANCE || 0.01, // Tolerance level for convergence
        },
    },

    // Quantum network settings
    network: {
        provider: process.env.QUANTUM_NETWORK_PROVIDER || 'http://quantum-network.example.com', // Default quantum network provider
        timeout: process.env.QUANTUM_NETWORK_TIMEOUT || 30000, // Timeout for network requests in milliseconds
    },
};

module.exports = quantumConfig;
