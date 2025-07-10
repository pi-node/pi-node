// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IncentiveProgram {
    address public owner;
    mapping(address => uint256) public rewards;
    uint256 public rewardCap; // Maximum reward cap per address

    event RewardGranted(address indexed supernode, uint256 amount);
    event RewardClaimed(address indexed claimant, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    constructor(uint256 _rewardCap) {
        owner = msg.sender; // Set the contract deployer as the owner
        rewardCap = _rewardCap; // Set the maximum reward cap
    }

    function rewardSupernode(address supernode, uint256 amount) public onlyOwner {
        require(amount <= rewardCap, "Amount exceeds reward cap");
        rewards[supernode] += amount;
        emit RewardGranted(supernode, amount); // Emit event for rewarding
    }

    function claimReward() public {
        uint256 rewardAmount = rewards[msg.sender];
        require(rewardAmount > 0, "No rewards available");
        rewards[msg.sender] = 0;

        // Use call to transfer Ether safely
        (bool success, ) = payable(msg.sender).call{value: rewardAmount}("");
        require(success, "Transfer failed");

        emit RewardClaimed(msg.sender, rewardAmount); // Emit event for claiming
    }

    // Emergency function to withdraw funds from the contract
    function emergencyWithdraw(uint256 amount) public onlyOwner {
        require(amount <= address(this).balance, "Insufficient balance");
        (bool success, ) = payable(owner).call{value: amount}("");
        require(success, "Transfer failed");
    }

    // Fallback function to receive Ether
    receive() external payable {}
}
