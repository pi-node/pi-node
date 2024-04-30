# pi-node API Documentation

This guide provides information about the pi-node IoT platform's API.

## Base URL

The base URL for the API is `http://localhost:3000/api`.

## Authentication

The pi-node API uses JWT for authentication. To authenticate, include the `Authorization` header with a valid JWT token.

## API Endpoints

### Device Management

- `GET /devices`: Retrieve a list of devices

  **Query Parameters**

  - `limit`: The maximum number of results to return (default: 10, max: 100)
  - `offset`: The starting point for the results (default: 0)

  **Example Request**

- GET /api/devices?limit=20&offset=10 Authorization: Bearer <JWT_TOKEN>

```
- `POST /devices`: Create a new device

**Request Body**

```json
{
  "name": "Device Name",
  "type": "Device Type",
  "configuration": {
    "property1": "value1",
    "property2": "value2"
  }
}
```
Example Request

```
POST /api/devices
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "name": "Device Name",
  "type": "Device Type",
  "configuration": {
    "property1": "value1",
    "property2": "value2"
  }
}
```

- GET /devices/:id: Retrieve a device by ID

Example Request
```
GET /api/devices/123
Authorization: Bearer <JWT_TOKEN>
```

- PUT /devices/:id: Update a device by ID

Request Body 
```
{
  "name": "Updated Device Name",
  "type": "Updated Device Type",
  "configuration": {
    "property1": "updatedValue1",
    "property2": "updatedValue2"
  }
}
```

Example Request

```
PUT /api/devices/123
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "name": "Updated Device Name",
  "type": "Updated Device Type",
  "configuration": {
    "property1": "updatedValue1",
    "property2": "updatedValue2"
  }
}
```

- DELETE /devices/:id: Delete a device by ID

Example Request

```
DELETE /api/devices/123
Authorization: Bearer <JWT_TOKEN>
```

# API Responses

Successful Response

A successful response will have a 200 OK status code and a JSON object containing the requested data.

Example Successful Response

```
{
  "data": [
    {
      "id": 1,
      "name": "Device Name",
      "type": "Device Type",
      "configuration": {
        "property1": "value1",
        "property2": "value2"
      }
    },
    {
      "id": 2,
      "name": "Device Name 2",
      "type": "Device Type 2",
      "configuration": {
        "property1": "value3",
        "property2": "value4"
      }
    }
  ]
}
```

Error Response

An error response will have a 4xx or 5xx status code and a JSON object containing an error message.

Example Error Response

```
{
  "error": {
    "message": "Device not found",
    "statusCode": 404
  }
}
```

