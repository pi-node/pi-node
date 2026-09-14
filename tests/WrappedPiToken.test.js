// test/WrappedPiToken.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("WrappedPiToken", function () {
    let WrappedPiToken;
    let wrappedPiToken;
    let PiToken;
    let piToken;
    let owner;
    let user1;
    let user2;

    const initialSupply = ethers.utils.parseUnits("1000", 18); // 1000 Pi tokens

    beforeEach(async function () {
        // Get the signers
        [owner, user1, user2] = await ethers.getSigners();

        // Deploy the PiToken contract
        const PiTokenFactory = await ethers.getContractFactory("ERC20"); // Assuming ERC20 is the PiToken implementation
        piToken = await PiTokenFactory.deploy("Pi Token", "PI", initialSupply);
        await piToken.deployed();

        // Deploy the WrappedPiToken contract
        WrappedPiToken = await ethers.getContractFactory("WrappedPiToken");
        wrappedPiToken = await WrappedPiToken.deploy(piToken.address);
        await wrappedPiToken.deployed();

        // Transfer some Pi tokens to user1 for testing
        await piToken.transfer(user1.address, ethers.utils.parseUnits("100", 18)); // Transfer 100 Pi tokens to user1
    });

    describe("Wrap Tokens", function () {
        it("should wrap Pi tokens correctly", async function () {
            const amountToWrap = ethers.utils.parseUnits("50", 18);

            // Approve the WrappedPiToken contract to spend Pi tokens
            await piToken.connect(user1).approve(wrappedPiToken.address, amountToWrap);

            // Wrap the tokens
            await wrappedPiToken.connect(user1).wrap(amountToWrap);

            // Check balances
            expect(await wrappedPiToken.balanceOf(user1.address)).to.equal(amountToWrap);
            expect(await piToken.balanceOf(wrappedPiToken.address)).to.equal(amountToWrap);
            expect(await piToken.balanceOf(user1.address)).to.equal(ethers.utils.parseUnits("50", 18)); // 100 - 50 = 50
        });

        it("should fail if user tries to wrap more tokens than they have", async function () {
            const amountToWrap = ethers.utils.parseUnits("200", 18); // More than user1 has

            await piToken.connect(user1).approve(wrappedPiToken.address, amountToWrap);

            await expect(wrappedPiToken.connect(user1).wrap(amountToWrap)).to.be.revertedWith("Insufficient Pi token balance");
        });
    });

    describe("Unwrap Tokens", function () {
        beforeEach(async function () {
            // Wrap some tokens before testing unwrapping
            const amountToWrap = ethers.utils.parseUnits("50", 18);
            await piToken.connect(user1).approve(wrappedPiToken.address, amountToWrap);
            await wrappedPiToken.connect(user1).wrap(amountToWrap);
        });

        it("should unwrap Wrapped Pi tokens correctly", async function () {
            const amountToUnwrap = ethers.utils.parseUnits("50", 18);

            // Unwrap the tokens
            await wrappedPiToken.connect(user1).unwrap(amountToUnwrap);

            // Check balances
            expect(await wrappedPiToken.balanceOf(user1.address)).to.equal(0);
            expect(await piToken.balanceOf(user1.address)).to.equal(ethers.utils.parseUnits("100", 18)); // 50 + 50 = 100
            expect(await piToken.balanceOf(wrappedPiToken.address)).to.equal(0);
        });

        it("should fail if user tries to unwrap more tokens than they have", async function () {
            const amountToUnwrap = ethers.utils.parseUnits("100", 18); // More than user1 has

            await expect(wrappedPiToken.connect(user1).unwrap(amountToUnwrap)).to.be.revertedWith("Insufficient Wrapped Pi Token balance");
        });
    });

    describe("Get Pi Token Balance", function () {
        it("should return the correct balance of Pi tokens held by the WrappedPiToken contract", async function () {
            const amountToWrap = ethers.utils.parseUnits("50", 18);
            await piToken.connect(user1).approve(wrappedPiToken.address, amountToWrap);
            await wrappedPiToken.connect(user1).wrap(amountToWrap);

            expect(await wrappedPiToken.getPiTokenBalance()).to.equal(amountToWrap);
        });
    });
});
