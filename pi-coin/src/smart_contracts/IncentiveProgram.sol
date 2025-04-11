// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IncentiveProgram {
    mapping(address => uint256) public rewards;
    address public admin;
    uint256 public totalRewardsDistributed;
    uint256 public minimumRewardAmount;

    event Rewarded(address indexed user, uint256 amount);
    event Claimed(address indexed user, uint256 amount);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    constructor(uint256 _minimumRewardAmount) {
        admin = msg.sender; // Set the contract deployer as the admin
        minimumRewardAmount = _minimumRewardAmount; // Set the minimum reward amount
    }

    function rewardUser (address user, uint256 amount) public onlyAdmin {
        require(amount >= minimumRewardAmount, "Reward amount is below the minimum threshold");
        rewards[user] += amount;
        totalRewardsDistributed += amount; // Track total rewards distributed
        emit Rewarded(user, amount); // Emit event for rewarding
    }

    function claimReward() public {
        uint256 rewardAmount = rewards[msg.sender];
        require(rewardAmount > 0, "No rewards available");
        rewards[msg.sender] = 0; // Reset the user's reward balance
        payable(msg.sender).transfer(rewardAmount); // Transfer the reward
        emit Claimed(msg.sender, rewardAmount); // Emit event for claiming
    }

    // Function to withdraw contract balance (only for admin)
    function withdraw(uint256 amount) public onlyAdmin {
        require(address(this).balance >= amount, "Insufficient balance");
        payable(admin).transfer(amount);
    }

    // Fallback function to receive Ether
    receive() external payable {}
}
