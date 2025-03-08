// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Migrations is Ownable {
    uint256 public lastCompletedMigration; // Tracks the last completed migration
    mapping(uint256 => bool) public migrationStatus; // Tracks the status of each migration

    event MigrationCompleted(uint256 indexed migrationId);
    event MigrationStatusUpdated(uint256 indexed migrationId, bool status);

    // Function to set the last completed migration
    function setCompleted(uint256 completed) external onlyOwner {
        require(completed > lastCompletedMigration, "Migration already completed");
        lastCompletedMigration = completed;
        migrationStatus[completed] = true; // Mark this migration as completed
        emit MigrationCompleted(completed);
        emit MigrationStatusUpdated(completed, true);
    }

    // Function to check if a migration has been completed
    function isMigrationCompleted(uint256 migrationId) external view returns (bool) {
        return migrationStatus[migrationId];
    }
}
