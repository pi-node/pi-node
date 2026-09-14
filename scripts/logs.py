import logging

def log_node():
    # Set up logging
    logging.basicConfig(filename='/var/log/pi-node.log', level=logging.INFO)

    # Log node events
    logging.info("Node started")
    logging.info("Node stopped")

if __name__ == "__main__":
    log_node()
