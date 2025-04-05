# Data Storage Service

This service provides data storage functionality for the pi-node IoT platform.

## Usage

To start the service, run the following command:

docker-compose up data-storage

````

The service will be available at `jdbc:postgresql://localhost:5432/data_storage`.

## Configuration

The service can be configured using environment variables or a configuration file.

### Environment Variables

- `POSTGRES_HOST`: The hostname of the database server
- `POSTGRES_PORT`: The port of the database server
- `POSTGRES_NAME`: The name of the database
- `POSTGRES_USER`: The username for the database
- `POSTGRES_PASSWORD`: The password for the database

### Configuration File

The service can also be configured using a configuration file in YAML format. The file should be named `config.yml` and placed in the root directory of the service.

```yaml
database:
  host: localhost
  port: 5432
  name: data_storage
  user: data_storage
  password: password
````

# Logging

The service logs messages to the console and to a file named data-storage.log. The log level can be configured using the LOG_LEVEL environment variable or the logging.level configuration option.

# Server

The service runs on a PostgreSQL server and listens on port 5432. The server can be configured using the POSTGRES_HOST, POSTGRES_PORT, POSTGRES_NAME, POSTGRES_USER, and POSTGRES_PASSWORD environment variables or the database configuration option.
