// contractDeployer.js
const { ethers } = require("hardhat");

async function main() {
    // Validate environment variables
    const tokenAddress = process.env.TOKEN_CONTRACT_ADDRESS;
    if (!tokenAddress) {
        throw new Error("Environment variable TOKEN_CONTRACT_ADDRESS is required.");
    }

    // Get the gas price and limit from environment variables or set defaults
    const gasPrice = process.env.GAS_PRICE ? ethers.utils.parseUnits(process.env.GAS_PRICE, 'gwei') : ethers.utils.parseUnits('20', 'gwei');
    const gasLimit = process.env.GAS_LIMIT || 3000000; // Default gas limit

    // Get the Governance contract factory
    const Governance = await ethers.getContractFactory("Governance");

    // Deploy the contract
    console.log("Deploying Governance contract...");
    const governanceContract = await Governance.deploy(tokenAddress, {
        gasLimit: gasLimit,
        gasPrice: gasPrice,
    });

    // Wait for the contract to be deployed
    await governanceContract.deployed();

    // Log the contract address and transaction hash
    console.log("Governance contract deployed to:", governanceContract.address);
    console.log("Transaction Hash:", governanceContract.deployTransaction.hash);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Deployment failed:", error);
        process.exit(1);
    });
