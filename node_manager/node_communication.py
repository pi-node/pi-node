import socket
import json
import logging
import asyncio

# Configure logging
logging.basicConfig(filename='node_communication.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NodeCommunication:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.server = None

    async def start_server(self):
        """Start the UDP server to listen for incoming messages."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))
        logging.info(f"Server started at {self.host}:{self.port}")

        while True:
            data, addr = await self.loop.run_in_executor(None, self.server.recvfrom, 1024)
            message = data.decode('utf-8')
            logging.info(f"Received message from {addr}: {message}")
            await self.handle_message(message, addr)

    async def handle_message(self, message, addr):
        """Handle incoming messages and respond accordingly."""
        try:
            data = json.loads(message)
            response = self.process_request(data)
            self.send_response(response, addr)
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON message.")
            self.send_response({"error": "Invalid JSON"}, addr)

    def process_request(self, data):
        """Process the incoming request and generate a response."""
        # Example processing logic
        if 'command' in data:
            command = data['command']
            logging.info(f"Processing command: {command}")
            return {"status": "success", "command": command}
        return {"error": "Unknown command"}

    def send_response(self, response, addr):
        """Send a response back to the client."""
        response_message = json.dumps(response).encode('utf-8')
        self.server.sendto(response_message, addr)
        logging.info(f"Sent response to {addr}: {response}")

    def run(self):
        """Run the UDP server."""
        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(self.start_server())
        except KeyboardInterrupt:
            logging.info("Server stopped by user.")
        finally:
            self.server.close()
            logging.info("Server closed.")

if __name__ == "__main__":
    node_comm = NodeCommunication()
    node_comm.run()
