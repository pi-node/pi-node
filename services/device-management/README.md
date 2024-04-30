# Device Management Service

This service provides device management functionality for the pi-node IoT platform.

## Usage

To start the service, run the following command:

docker-compose up device-management

```

The service will be available at `http://localhost:3001`.

## API

The service provides the following API endpoints:

- `GET /devices`: Retrieve a list of devices
- `POST /devices`: Create a new device
- `GET /devices/:id`: Retrieve a device by ID
- `PUT /devices/:id`: Update a device by ID
- `DELETE /devices/:id`: Delete a device by ID

## Configuration

The service can be configured using environment variables or a configuration file.

### Environment Variables

- `DATABASE_HOST`: The hostname of the database server
- `DATABASE_PORT`: The port of the database server
- `DATABASE_NAME`: The name of the database
- `DATABASE_USER`: The username for the database
- `DATABASE_PASSWORD`: The password for the database
- `MESSAGE_BROKER_HOST`: The hostname of the message broker server
- `MESSAGE_BROKER_PORT`: The port of the message broker server
- `MESSAGE_BROKER_USERNAME`: The username for the message broker
- `MESSAGE_BROKER_PASSWORD`: The password for the message broker
- `SERVICE_REGISTRY_HOST`: The hostname of the service registry server
- `SERVICE_REGISTRY_PORT`: The port of the service registry server

### Configuration File

The service can also be configured using a configuration file in YAML format. The file should be named `config.yml` and placed in the root directory of the service.

```yaml
database:
  host: localhost
  port: 5432
  name: device_management
  user: device_management
  password: password
messageBroker:
  host: message_broker
  port: 5672
  username: rabbitmq
  password: password
serviceRegistry:
  host: service_registry
  port: 8761
```

# Logging
The service logs messages to the console and to a file named device-management.log. The log level can be configured using the LOG_LEVEL environment variable or the logging.level configuration option.

Server
The service runs on a Node.js server and listens on port 3001. The server can be configured using the SERVER_HOST and SERVER_PORT environment variables or the server.host and server.port configuration options.


Create an `api/index.js` file to define the API entry point:

```
const express = require('express');
const router = express.Router();

// Import API routes
const devices = require('./routes/devices');

// Register API routes
router.use('/devices', devices);

module.exports = router;
```

Create a routes/ directory for API routes and a controllers/ directory for API controllers.

Create a models/ directory for data models and a services/ directory for external service calls.
  
