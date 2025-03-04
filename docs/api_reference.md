# Pi Supernode API Reference

## Overview

The Pi Supernode API provides a set of endpoints for interacting with the Pi Coin ecosystem. This document outlines the available API endpoints, their methods, parameters, and response formats.

## Base URL

The base URL for the API is:

```
http://localhost:3000/api
```

## Authentication

Currently, the API does not require authentication. However, it is recommended to implement authentication for production environments.

## Endpoints

### 1. Get Balance

- **Endpoint**: `/balance/:address`
- **Method**: `GET`
- **Description**: Retrieve the balance of a specific account.
- **URL Parameters**:
  - `address` (string): The public address of the account.
- **Response**:
  - **Status Code**: `200 OK`
  - **Content**:
    ```json
    {
      "success": true,
      "balance": [
        {
          "asset_type": "native",
          "balance": "100.00"
        },
        {
          "asset_type": "PiCoin",
          "balance": "50.00"
        }
      ]
    }
    ```
  - **Status Code**: `404 Not Found`
  - **Content**:
    ```json
    {
      "success": false,
      "error": "Account not found."
    }
    ```

### 2. Send Pi Coin

- **Endpoint**: `/send`
- **Method**: `POST`
- **Description**: Send Pi Coin from one account to another.
- **Request Body**:
  ```json
  {
    "senderSecret": "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "receiverPublicKey": "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "amount": "10"
  }
  ```
- **Response**:
  - **Status Code**: `200 OK`
  - **Content**:
    ```json
    {
      "success": true,
      "result": {
        "hash": "transaction_hash_here",
        "status": "completed"
      }
    }
    ```
  - **Status Code**: `400 Bad Request`
  - **Content**:
    ```json
    {
      "success": false,
      "error": "Invalid transaction parameters."
    }
    ```

### 3. Create Proposal

- **Endpoint**: `/propose`
- **Method**: `POST`
- **Description**: Create a new governance proposal.
- **Request Body**:
  ```json
  {
    "title": "New Proposal",
    "description": "Details about the proposal."
  }
  ```
- **Response**:
  - **Status Code**: `201 Created`
  - **Content**:
    ```json
    {
      "success": true,
      "proposal": {
        "id": "proposal_id_here",
        "title": "New Proposal",
        "description": "Details about the proposal."
      }
    }
    ```
  - **Status Code**: `400 Bad Request`
  - **Content**:
    ```json
    {
      "success": false,
      "error": "Proposal title and description are required."
    }
    ```

### 4. Vote on Proposal

- **Endpoint**: `/vote`
- **Method**: `POST`
- **Description**: Vote on a governance proposal.
- **Request Body**:
  ```json
  {
    "proposalId": "proposal_id_here",
    "vote": "yes" // or "no"
  }
  ```
- **Response**:
  - **Status Code**: `200 OK`
  - **Content**:
    ```json
    {
      "success": true,
      "result": {
        "proposalId": "proposal_id_here",
        "vote": "yes"
      }
    }
    ```
  - **Status Code**: `404 Not Found`
  - **Content**:
    ```json
    {
      "success": false,
      "error": "Proposal not found."
    }
    ```

## Error Handling

All API responses include a `success` field indicating whether the request was successful. In case of an error, the response will include an `error` field with a description of the issue.

## Conclusion

This API reference provides a comprehensive overview of the available endpoints in the Pi Supernode project. For further assistance or to report issues, please refer to the project's documentation or reach out to the community.
