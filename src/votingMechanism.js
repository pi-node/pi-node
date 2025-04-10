// votingMechanism.js
const { ethers } = require("hardhat");

async function voteOnProposal(governanceContract, proposalId, voterAddress) {
    try {
        // Check if the proposal is active
        const proposal = await governanceContract.proposals(proposalId);
        if (Date.now() / 1000 >= proposal.endTime) {
            throw new Error("Voting has ended for this proposal.");
        }

        // Check if the voter has already voted
        const hasVoted = await governanceContract.voters(proposalId, voterAddress);
        if (hasVoted) {
            throw new Error("You have already voted on this proposal.");
        }

        // Get the voter's token balance
        const voterTokenBalance = await governanceContract.token().balanceOf(voterAddress);
        if (voterTokenBalance.isZero()) {
            throw new Error("You must hold tokens to vote.");
        }

        // Cast the vote
        const tx = await governanceContract.vote(proposalId, { from: voterAddress });
        await tx.wait();

        console.log(`Voter ${voterAddress} has successfully voted on proposal ${proposalId}`);
    } catch (error) {
        console.error(`Error voting on proposal ${proposalId}: ${error.message}`);
    }
}

async function voteOnMultipleProposals(governanceContract, proposalIds, voterAddress) {
    try {
        for (const proposalId of proposalIds) {
            await voteOnProposal(governanceContract, proposalId, voterAddress);
        }
        console.log(`Voter ${voterAddress} has voted on multiple proposals: ${proposalIds.join(", ")}`);
    } catch (error) {
        console.error(`Error voting on multiple proposals: ${error.message}`);
    }
}

module.exports = {
    voteOnProposal,
    voteOnMultipleProposals,
};
