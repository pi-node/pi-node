# Pi Supernode User Guide

## Overview

The Pi Supernode is a decentralized application designed to enhance the security and efficiency of transactions within the Pi Network. This user guide provides instructions on how to set up and use the Pi Supernode effectively.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Using the API](#using-the-api)
6. [Governance Features](#governance-features)
7. [Monitoring the System](#monitoring-the-system)
8. [Troubleshooting](#troubleshooting)
9. [Conclusion](#conclusion)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 14 or higher)
- **npm** (Node Package Manager)
- **Git** (for cloning the repository)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KOSASIH/pi-supernode.git
   cd pi-supernode
   ```

2. **Run the Setup Script**:
   This script will install the necessary dependencies and create the required files.
   ```bash
   bash scripts/setup.sh
   ```

## Configuration

1. **Create a `.env` File**:
   Copy the `.env.example` file to `.env` and update the values as needed.
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` File**:
   Open the `.env` file and configure the following variables:
   ```plaintext
   PORT=3000
   STELLAR_HORIZON_URL=https://horizon-testnet.stellar.org
   PI_COIN_ASSET_CODE=PiCoin
   PI_COIN_ISSUER=GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

## Running the Application

To start the Pi Supernode application, run the following command:

```bash
npm start
```

The application will start and listen on the specified port (default is 3000).

## Using the API

The Pi Supernode provides a RESTful API for interacting with the system. Below are some common API endpoints:

### 1. Get Balance

- **Endpoint**: `GET /api/balance/:address`
- **Description**: Retrieve the balance of a specific account.
- **Example**:
  ```bash
  curl http://localhost:3000/api/balance/GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  ```

### 2. Send Pi Coin

- **Endpoint**: `POST /api/send`
- **Description**: Send Pi Coin from one account to another.
- **Request Body**:
  ```json
  {
    "senderSecret": "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "receiverPublicKey": "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "amount": "10"
  }
  ```
- **Example**:
  ```bash
  curl -X POST http://localhost:3000/api/send -H "Content-Type: application/json" -d '{"senderSecret":"SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX","receiverPublicKey":"GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX","amount":"10"}'
  ```

## Governance Features

The Pi Supernode allows users to participate in governance by proposing changes and voting on proposals.

### 1. Create Proposal

- **Endpoint**: `POST /api/propose`
- **Description**: Create a new governance proposal.
- **Request Body**:
  ```json
  {
    "title": "New Proposal",
    "description": "Details about the proposal."
  }
  ```

### 2. Vote on Proposal

- **Endpoint**: `POST /api/vote`
- **Description**: Vote on a governance proposal.
- **Request Body**:
  ```json
  {
    "proposalId": "123",
    "vote": "yes"
  }
  ```

## Monitoring the System

To monitor the application, you can use the provided monitoring script:

```bash
bash scripts/monitor.sh
```

This script will check the application status, monitor logs, and track system resource usage.

## Troubleshooting

- **Application Not Starting**: Ensure that all dependencies are installed and that the `.env` file is correctly configured.
- **API Errors**: Check the application logs for detailed error messages. You can find logs in the `logs` directory.

## Conclusion

The Pi Supernode provides a robust platform for managing Pi Coin transactions and governance. By following this user guide, you should be able to set up, configure, and use the system effectively. For further assistance, please refer to the project's documentation or reach out to the community.
