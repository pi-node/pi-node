// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Migrations is Ownable {
    uint256 public last_completed_migration;

    event MigrationCompleted(uint256 completed);

    // Function to set the completed migration
    function setCompleted(uint256 completed) public onlyOwner {
        last_completed_migration = completed;
        emit MigrationCompleted(completed);
    }

    // Function to get the last completed migration
    function getLastCompletedMigration() public view returns (uint256) {
        return last_completed_migration;
    }
}
