# edge_protocol.py
import enum

class EdgeProtocol(enum.Enum):
    COAP = 1
    MQTT = 2
    HTTP = 3

    def __init__(self, protocol: str):
        self.protocol = protocol

    def send_request(self, request: str) -> None:
        # Send request using edge protocol
        pass

    def receive_response(self) -> str:
        # Receive response using edge protocol
        pass
