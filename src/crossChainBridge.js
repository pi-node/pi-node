// crossChainBridge.js
const { ethers } = require("hardhat");

class CrossChainBridge {
    constructor(piCoinContract, targetChain) {
        this.piCoinContract = piCoinContract; // Pi Coin contract instance
        this.targetChain = targetChain; // Target blockchain for transfer
    }

    async transferToTargetChain(amount, recipientAddress) {
        try {
            // Check if the sender has enough balance
            const senderAddress = await this.piCoinContract.signer.getAddress();
            const balance = await this.piCoinContract.balanceOf(senderAddress);
            if (balance.lt(amount)) {
                throw new Error("Insufficient balance for transfer.");
            }

            // Approve the transfer
            await this.piCoinContract.approve(this.targetChain.bridgeAddress, amount);

            // Execute the transfer
            const tx = await this.targetChain.bridgeContract.transfer(amount, recipientAddress);
            await tx.wait();

            console.log(`Transferred ${amount.toString()} Pi Coin to ${recipientAddress} on ${this.targetChain.name}`);
        } catch (error) {
            console.error("Error during cross-chain transfer:", error.message);
        }
    }
}

module.exports = CrossChainBridge;
