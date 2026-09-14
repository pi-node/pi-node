const express = require('express');
const axios = require('axios');
const winston = require('winston');
const Web3 = require('web3'); // For Ethereum-based blockchains
const { ethers } = require('ethers'); // For Ethereum-based blockchains
const { ChainId, Token, Fetcher, Route, Trade, TokenAmount, TradeType } = require('@uniswap/sdk'); // For Uniswap integration

class IntegrationEngine {
  constructor(config) {
    this.config = config;
    this.setupLogger();
    this.setupExpress();
    this.web3 = new Web3(new Web3.providers.HttpProvider(this.config.ethereum.nodeUrl));
    this.provider = new ethers.providers.JsonRpcProvider(this.config.ethereum.nodeUrl);
  }

  setupLogger() {
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
      ),
      transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'integration_engine.log' })
      ]
    });
  }

  setupExpress() {
    this.app = express();
    this.app.use(express.json());

    // Define API routes
    this.app.post('/api/sendTransaction', this.sendTransaction.bind(this));
    this.app.get('/api/getBalance/:address', this.getBalance.bind(this));
    this.app.get('/api/queryTransaction/:txHash', this.queryTransaction.bind(this));
    this.app.post('/api/swapTokens', this.swapTokens.bind(this));
    this.app.get('/api/health', this.healthCheck.bind(this));

    this.app.listen(this.config.port, () => {
      this.logger.info(`Integration Engine API listening on port ${this.config.port}`);
    });
  }

  async sendTransaction(req, res) {
    const { from, to, value, privateKey } = req.body;

    try {
      const account = this.web3.eth.accounts.privateKeyToAccount(privateKey);
      const nonce = await this.web3.eth.getTransactionCount(from);
      const gasPrice = await this.web3.eth.getGasPrice();
      const gasLimit = this.config.gasLimit || 21000; // Use configured gas limit or default

      const tx = {
        from: account.address,
        to,
        value: this.web3.utils.toWei(value, 'ether'),
        gas: gasLimit,
        gasPrice,
        nonce
      };

      const signedTx = await this.web3.eth.accounts.signTransaction(tx, privateKey);
      const receipt = await this.web3.eth.sendSignedTransaction(signedTx.rawTransaction);
      this.logger.info(`Transaction successful: ${receipt.transactionHash}`);
      res.json({ success: true, transactionHash: receipt.transactionHash });
    } catch (error) {
      this.logger.error('Error sending transaction:', error);
      res.status(500).json({ success: false, error: error.message });
    }
  }

  async getBalance(req, res) {
    const { address } = req.params;

    try {
      const balance = await this.web3.eth.getBalance(address);
      const balanceInEther = this.web3.utils.fromWei(balance, 'ether');
      res.json({ address, balance: balanceInEther });
    } catch (error) {
      this.logger.error('Error fetching balance:', error);
      res.status(500).json({ success: false, error: error.message });
    }
  }

  async queryTransaction(req, res) {
    const { txHash } = req.params;

    try {
      const receipt = await this.web3.eth.getTransactionReceipt(txHash);
      if (receipt) {
        res.json({ success: true, receipt });
      } else {
        res.status(404).json({ success: false, error: 'Transaction not found' });
      }
    } catch (error) {
      this.logger.error('Error querying transaction:', error);
      res.status(500).json ({ success: false, error: error.message });
    }
  }

  async swapTokens(req, res) {
    const { tokenIn, tokenOut, amountIn, recipient, privateKey } = req.body;

    try {
      const tokenA = await Fetcher.fetchTokenData(ChainId.MAINNET, tokenIn);
      const tokenB = await Fetcher.fetchTokenData(ChainId.MAINNET, tokenOut);
      const amountInToken = new TokenAmount(tokenA, this.web3.utils.toWei(amountIn, 'ether'));
      const pair = await Fetcher.fetchPairData(tokenA, tokenB);
      const route = new Route([pair], tokenA);
      const trade = new Trade(route, amountInToken, TradeType.EXACT_INPUT);
      const amountOut = trade.outputAmount.toFixed();

      // Logic to create and send the swap transaction
      this.logger.info(`Swapping ${amountIn} of ${tokenIn} for ${amountOut} of ${tokenOut}`);
      // Transaction creation and signing logic goes here

      res.json({ success: true, amountOut });
    } catch (error) {
      this.logger.error('Error swapping tokens:', error);
      res.status(500).json({ success: false, error: error.message });
    }
  }

  async healthCheck(req, res) {
    res.json({ status: 'Integration Engine is running', port: this.config.port });
  }

  async listenForEvents() {
    this.provider.on('block', (blockNumber) => {
      this.logger.info(`New block mined: ${blockNumber}`);
    });
  }
}

module.exports = IntegrationEngine;
