// src/constant.js

const PI_COIN = {
    SYMBOL: "PI",
    VALUE: 314159.00, // Fixed value of Pi Coin in USD
    SUPPLY: 100_000_000_000, // Total supply of Pi Coin (100 billion for enhanced market cap)
    DYNAMIC_SUPPLY: true, // Enable dynamic supply adjustments for unparalleled market responsiveness
    IS_STABLECOIN: true, // Indicates that Pi Coin is a stablecoin
    STABILITY_MECHANISM: "Multi-Asset Collateralized with Algorithmic and Market-Driven Adjustments", // Mechanism for maintaining stability
    COLLATERAL_RATIO: 10.0, // Enhanced collateralization ratio for increased stability
    TRANSACTION_FEE: 0.00000001, // Ultra-low transaction fee in USD for user engagement
    BLOCK_TIME: 0.0001, // Ultra-fast average block time in seconds for instant transactions
    MINING_REWARD: 1000000, // Substantial reward for mining a block to incentivize participation
    DECIMALS: 42, // Number of decimal places for Pi Coin
    GENESIS_BLOCK_TIMESTAMP: "2025-01-01T00:00:00Z", // Timestamp of the genesis block

    // Governance features
    GOVERNANCE_MODEL: {
        TYPE: "Decentralized Autonomous Organization (DAO)", // Governance model
        VOTING_SYSTEM: "Quadratic Voting", // Voting mechanism
        VOTING_PERIOD: 86400, // Voting period in seconds (1 day)
        PROPOSAL_THRESHOLD: 1000, // Minimum tokens required to create a proposal
    },

    // Security features
    SECURITY: {
        TWO_FACTOR_AUTHENTICATION: true, // Enable two-factor authentication for added security
        PHISHING_PROTECTION: true, // Implement measures to protect against phishing attacks
        REGULAR_SECURITY_UPDATES: true, // Ensure regular updates to security protocols
        ADVANCED_FRAUD_DETECTION: true, // Implement advanced fraud detection mechanisms
    },

    // Network features
    NETWORK: {
        PROTOCOL: "Hybrid PoS + DPoS + Sharding + Layer 2 Solutions", // Advanced network protocol for scalability
        MAX_PEERS: 1000, // Maximum number of peers in the network
        NODE_TIMEOUT: 5000, // Timeout for node responses in milliseconds
        CONNECTION_RETRY_INTERVAL: 1000, // Retry interval for node connections in milliseconds
    },

    // Additional features
    SMART_CONTRACT_SUPPORT: true, // Enable smart contract functionality
    INTEROPERABILITY: true, // Support for cross-chain transactions
    USER_PRIVACY_CONTROL: true, // Allow users to control their privacy settings
    AI_INTEGRATION: true, // Incorporate AI for predictive analytics and decision-making
    ENVIRONMENTAL_SUSTAINABILITY: true, // Focus on sustainable practices in operations
};

module.exports = PI_COIN;
