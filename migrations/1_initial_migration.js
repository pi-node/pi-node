// migrations/1_initial_migration.js

const WrappedPiToken = artifacts.require("WrappedPiToken");
const PiToken = artifacts.require("ERC20"); // Assuming ERC20 is the implementation of your PiToken

module.exports = async function (deployer) {
    // Deploy the PiToken contract
    const initialSupply = web3.utils.toWei("1000000", "ether"); // 1,000,000 Pi tokens
    await deployer.deploy(PiToken, "Pi Token", "PI", initialSupply);
    const piTokenInstance = await PiToken.deployed();

    // Deploy the WrappedPiToken contract with the address of the PiToken
    await deployer.deploy(WrappedPiToken, piTokenInstance.address);
    const wrappedPiTokenInstance = await WrappedPiToken.deployed();

    console.log(`PiToken deployed at: ${piTokenInstance.address}`);
    console.log(`WrappedPiToken deployed at: ${wrappedPiTokenInstance.address}`);
};
