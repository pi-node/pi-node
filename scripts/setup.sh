#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to print messages
function print_message {
    echo "=============================="
    echo "$1"
    echo "=============================="
}

# Print welcome message
print_message "Setting up the Blockchain Application Environment"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_message "Node.js is not installed. Please install Node.js before running this script."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_message "npm is not installed. Please install npm before running this script."
    exit 1
fi

# Create project directories if they don't exist
mkdir -p src/{ai,blockchain,config,controllers,monitoring,routes,tests}
mkdir -p scripts

# Create a basic package.json file if it doesn't exist
if [ ! -f package.json ]; then
    print_message "Creating package.json"
    npm init -y
fi

# Install required dependencies
print_message "Installing required dependencies"
npm install express body-parser stellar-sdk dotenv express-validator

# Create a .env file with default values
if [ ! -f .env ]; then
    print_message "Creating .env file"
    cat <<EOL > .env
PORT=3000
STELLAR_HORIZON_URL=https://horizon-testnet.stellar.org
PI_COIN_ASSET_CODE=PiCoin
PI_COIN_ISSUER=GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
EOL
fi

# Create a README file
if [ ! -f README.md ]; then
    print_message "Creating README.md"
    cat <<EOL > README.md
# Blockchain Application

This is a blockchain application that utilizes Stellar SDK for handling transactions and governance proposals.

## Setup

1. Clone the repository.
2. Run \`bash scripts/setup.sh\` to set up the environment.
3. Start the application with \`node src/index.js\`.

## Environment Variables

- \`PORT\`: The port on which the server will run.
- \`STELLAR_HORIZON_URL\`: The URL for the Stellar Horizon server.
- \`PI_COIN_ASSET_CODE\`: The asset code for Pi Coin.
- \`PI_COIN_ISSUER\`: The issuer address for Pi Coin.
EOL
fi

# Print completion message
print_message "Setup completed successfully!"
