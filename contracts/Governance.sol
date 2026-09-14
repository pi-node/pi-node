// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Governance is Ownable {
    using SafeMath for uint256;

    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 voteCount;
        uint256 endTime;
        bool executed;
        mapping(address => bool) voters;
    }

    uint256 public proposalCount;
    uint256 public votingDuration; // Duration for voting in seconds
    mapping(uint256 => Proposal) public proposals;

    event ProposalCreated(uint256 id, address proposer, string description, uint256 endTime);
    event Voted(uint256 proposalId, address voter);
    event ProposalExecuted(uint256 proposalId);

    constructor(uint256 _votingDuration) {
        votingDuration = _votingDuration; // Set the voting duration
    }

    // Function to create a new proposal
    function createProposal(string memory description) external {
        proposalCount = proposalCount.add(1);
        Proposal storage newProposal = proposals[proposalCount];
        newProposal.id = proposalCount;
        newProposal.proposer = msg.sender;
        newProposal.description = description;
        newProposal.endTime = block.timestamp.add(votingDuration);
        newProposal.executed = false;

        emit ProposalCreated(proposalCount, msg.sender, description, newProposal.endTime);
    }

    // Function to vote on a proposal
    function vote(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp < proposal.endTime, "Voting has ended");
        require(!proposal.voters[msg.sender], "You have already voted");

        proposal.voters[msg.sender] = true;
        proposal.voteCount = proposal.voteCount.add(1);

        emit Voted(proposalId, msg.sender);
    }

    // Function to execute a proposal if it has enough votes
    function executeProposal(uint256 proposalId) external onlyOwner {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp >= proposal.endTime, "Voting is still ongoing");
        require(!proposal.executed, "Proposal has already been executed");
        require(proposal.voteCount > 0, "No votes received");

        // Execute the proposal logic here (e.g., change parameters, mint tokens, etc.)
        // This is a placeholder for actual execution logic.

        proposal.executed = true;
        emit ProposalExecuted(proposalId);
    }

    // Function to get the details of a proposal
    function getProposal(uint256 proposalId) external view returns (
        uint256 id,
        address proposer,
        string memory description,
        uint256 voteCount,
        uint256 endTime,
        bool executed
    ) {
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.id,
            proposal.proposer,
            proposal.description,
            proposal.voteCount,
            proposal.endTime,
            proposal.executed
        );
    }
}
