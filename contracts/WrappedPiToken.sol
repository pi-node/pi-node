// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract WrappedPiToken is ERC20Burnable, Ownable, ReentrancyGuard {
    IERC20 public piToken;

    // Events for logging
    event Wrapped(address indexed user, uint256 amount);
    event Unwrapped(address indexed user, uint256 amount);

    constructor(address _piToken) ERC20("Wrapped Pi Token", "WPI") {
        require(_piToken != address(0), "Invalid Pi token address");
        piToken = IERC20(_piToken);
    }

    /**
     * @dev Wraps Pi tokens into Wrapped Pi Tokens.
     * @param amount The amount of Pi tokens to wrap.
     */
    function wrap(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be greater than 0");
        require(piToken.balanceOf(msg.sender) >= amount, "Insufficient Pi token balance");

        // Transfer Pi tokens from the user to this contract
        piToken.transferFrom(msg.sender, address(this), amount);
        
        // Mint Wrapped Pi Tokens to the user
        _mint(msg.sender, amount);

        // Emit the Wrapped event
        emit Wrapped(msg.sender, amount);
    }

    /**
     * @dev Unwraps Wrapped Pi Tokens back into Pi tokens.
     * @param amount The amount of Wrapped Pi Tokens to unwrap.
     */
    function unwrap(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be greater than 0");
        require(balanceOf(msg.sender) >= amount, "Insufficient Wrapped Pi Token balance");

        // Burn Wrapped Pi Tokens from the user
        _burn(msg.sender, amount);
        
        // Transfer Pi tokens back to the user
        piToken.transfer(msg.sender, amount);

        // Emit the Unwrapped event
        emit Unwrapped(msg.sender, amount);
    }

    /**
     * @dev Returns the balance of Pi tokens held by this contract.
     * @return The balance of Pi tokens.
     */
    function getPiTokenBalance() external view returns (uint256) {
        return piToken.balanceOf(address(this));
    }
}
