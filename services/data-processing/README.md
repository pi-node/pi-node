# Data Processing Service

This service provides data processing functionality for the pi-node IoT platform.

## Usage

To start the service, run the following command:

docker-compose up data-processing

````

The service will be available at `http://localhost:3003`.

## API

The service provides the following API endpoints:

- `POST /data`: Process new data

## Configuration

The service can be configured using environment variables or a configuration file.

### Environment Variables

- `MESSAGE_BROKER_HOST`: The hostname of the message broker server
- `MESSAGE_BROKER_PORT`: The port of the message broker server
- `MESSAGE_BROKER_USERNAME`: The username for the message broker
- `MESSAGE_BROKER_PASSWORD`: The password for the message broker

### Configuration File

The service can also be configured using a configuration file in YAML format. The file should be named `config.yml` and placed in the root directory of the service.

```yaml
messageBroker:
  host: message_broker
  port: 5672
  username: rabbitmq
  password: password
````

# Logging

The service logs messages to the console and to a file named data-processing.log. The log level can be configured using the LOG_LEVEL environment variable or the logging.level configuration option.

# Server

The service runs on a Node.js server and listens on port 3003. The server can be configured using the SERVER_HOST and SERVER_PORT environment variables or the server.host and server.port configuration options.

````

**2. `services/user-management/`: User management service**

Create a `Dockerfile` to build a user management container:

```Dockerfile
FROM node:16

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the application code
COPY . .

# Set the default command
CMD ["npm", "start"]
````

# User Management Service

This service provides user management functionality for the pi-node IoT platform.

## Usage

To start the service, run the following command:

docker-compose up user-management

````

The service will be available at `http://localhost:3004`.

## API

The service provides the following API endpoints:

- `POST /users`: Create a new user
- `GET /users/:id`: Retrieve a user by ID
- `PUT /users/:id`: Update a user by ID
- `DELETE /users/:id`: Delete a user by ID

## Configuration

The service can be configured using environment variables or a configuration file.

### Environment Variables

- `DATABASE_HOST`: The hostname of the database server
- `DATABASE_PORT`: The port of the database server
- `DATABASE_NAME`: The name of the database
- `DATABASE_USER`: The username for the database
- `DATABASE_PASSWORD`: The password for the database

### Configuration File

The service can also be configured using a configuration file in YAML format. The file should be named `config.yml` and placed in the root directory of the service.

```yaml
database:
  host: localhost
  port: 5432
  name: user_management
  user: user_management
  password: password
````

# Logging

The service logs messages to the console and to a file named user-management.log. The log level can be configured using the LOG_LEVEL environment variable or the logging.level configuration option.

# Server

The service runs on a Node.js server and listens on port 3004. The server can be configured using the SERVER_HOST and SERVER_PORT environment variables or the server.host and server.port configuration options.

````

**3. `services/notifications/`: Notifications service**

Create a `Dockerfile` to build a notifications container:

```Dockerfile
FROM node:16

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the application code
COPY . .

# Set the default command
CMD ["npm", "start"]
````

# Notifications Service

This service provides notifications functionality for the pi-node IoT platform.

## Usage

To start the service, run the following command:

docker-compose up notifications

````


The service will be available at `http://localhost:3005`.

## API

The service provides the following API endpoints:

- `POST /notifications`: Send a new notification

## Configuration

The service can be configured using environment variables or a configuration file.

### Environment Variables

- `MESSAGE_BROKER_HOST`: The hostname of the message broker server
- `MESSAGE_BROKER_PORT`: The port of the message broker server
- `MESSAGE_BROKER_USERNAME`: The username for the message broker
- `MESSAGE_BROKER_PASSWORD`: The password for the message broker

### Configuration File

The service can also be configured using a configuration file in YAML format. The file should be named `config.yml` and placed in the root directory of the service.

```yaml
messageBroker:
  host: message_broker
  port: 5672
  username: rabbitmq
  password: password
````

# Logging

The service logs messages to the console and to a file named notifications.log. The log level can be configured using the LOG_LEVEL environment variable or the logging.level configuration option.

# Server

The service runs on a Node.js server and listens on port 3005. The server can be configured using the SERVER_HOST and SERVER_PORT environment variables or the server.host and server.port configuration options.

# Web Interface Service

This service provides the web interface for the pi-node IoT platform.

## Usage

To start the service, run the following command:

docker-compose up web-interface

````

The service will be available at `http://localhost:3000`.

## Configuration

The service can be configured using environment variables or a configuration file.

### Environment Variables

- `API_HOST`: The hostname of the API server
- `API_PORT`: The port of the API server

### Configuration File
The service can also be configured using a configuration file in YAML format. The file should be named `config.yml` and placed in the root directory of the service.

```yaml
api:
  host: localhost
  port: 3001
````

# Logging

The service logs messages to the console and to a file named web-interface.log. The log level can be configured using the LOG_LEVEL environment variable or the logging.level configuration option.

# Server

The service runs on a Node.js server and listens on port 3000. The server can be configured using the SERVER_HOST and SERVER_PORT environment variables or the server.host and server.port configuration options.

````
**5. `services/mobile-app/`: Mobile app service**

Create a `Dockerfile` to build a mobile app container:

```Dockerfile
FROM node:16

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the application code
COPY . .

# Set the default command
CMD ["npm", "start"]
````

# Mobile App Service

This service provides the mobile app for the pi-node IoT platform.

## Usage

To start the service, run the following command:

docker-compose up mobile-app

````

The service will be available at `http://localhost:3006`.

## Configuration

The service can be configured using environment variables or a configuration file.

### Environment Variables

- `API_HOST`: The hostname of the API server
- `API_PORT`: The port of the API server

### Configuration File

The service can also be configured using a configuration file in YAML format. The file should be named `config.yml` and placed in the root directory of the service.

```yaml
api:
  host: localhost
  port: 3001
````

# Logging

The service logs messages to the console and to a file named mobile-app.log. The log level can be configured using the LOG_LEVEL environment variable or the logging.level configuration option.

# Server

The service runs on a Node.js server and listens on port 3006. The server can be configured using the SERVER_HOST and SERVER_PORT environment variables or the server.host and server.port configuration options.
