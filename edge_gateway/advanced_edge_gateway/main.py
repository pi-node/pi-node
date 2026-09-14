import logging
import os
import json
from flask import Flask, jsonify
from temperature_sensor import TemperatureSensor  # Assuming this is a custom module for temperature readings
from node_registry import NodeRegistry
from node_monitor import NodeMonitor

# Configure logging
logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

class Supernode:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.temperature_sensor = TemperatureSensor(self.config.get('sensor_device_path', '/sys/bus/w1/devices/28-000005f8b8ff/w1_slave'))
        self.node_registry = NodeRegistry(uri=self.config.get('registry_uri', 'ws://localhost:8765'))
        self.node_monitor = NodeMonitor(uri=self.config.get('monitor_uri', 'ws://localhost:8765'))

    def load_config(self):
        """Load configuration from a JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                logging.info("Configuration loaded successfully.")
                return config
        else:
            logging.error(f"Configuration file {self.config_file} not found. Using default settings.")
            return {}

    def get_temperature(self):
        """Get the current temperature from the sensor."""
        try:
            temperature = self.temperature_sensor.read_temperature()
            logging.info(f"Current temperature: {temperature}°C")
            return temperature
        except Exception as e:
            logging.error(f"Error reading temperature: {e}")
            return None

    @app.route('/status', methods=['GET'])
    def status():
        """Endpoint to get the current status of the Raspberry Pi."""
        uptime = self.get_uptime()
        temperature = self.get_temperature()
        response = {
            'temperature': temperature,
            'uptime': uptime
        }
        return jsonify(response)

    def get_uptime(self):
        """Get the uptime of the Raspberry Pi."""
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime = self.format_uptime(uptime_seconds)
            return uptime

    def format_uptime(self, seconds):
        """Format uptime from seconds to a readable string."""
        days = int(seconds // (24 * 3600))
        hours = int((seconds % (24 * 3600)) // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{days} days, {hours} hours, {minutes} minutes"

    def run(self):
        """Run the Flask application."""
        try:
            logging.info("Starting the Supernode application...")
            app.run(host='0.0.0.0', port=3000)
        except Exception as e:
            logging.error(f"Error while running the application: {e}")

if __name__ == "__main__":
    supernode = Supernode()
    supernode.run()
