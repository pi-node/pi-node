const StableCoin = artifacts.require("StableCoin");
const PriceFeed = artifacts.require("PriceFeed"); // Assuming you have a PriceFeed contract

module.exports = async function (deployer) {
    // Deploy the PriceFeed contract first
    await deployer.deploy(PriceFeed);
    const priceFeedInstance = await PriceFeed.deployed();

    // Deploy the StableCoin contract with the address of the PriceFeed
    await deployer.deploy(StableCoin, priceFeedInstance.address);

    // Optionally log the addresses of the deployed contracts
    const stableCoinInstance = await StableCoin.deployed();
    console.log("PriceFeed deployed at:", priceFeedInstance.address);
    console.log("StableCoin deployed at:", stableCoinInstance.address);
};
