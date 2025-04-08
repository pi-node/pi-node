import socket

class SmartHomeAutomationClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def control_device(self, device, action):
        # Send request to control device
        self.socket.send(b"control_device")
        self.socket.send(device.encode())
        self.socket.send(action.encode())
        response = self.socket.recv(1024)
        return response

    def detect_motion(self):
        # Send request to detect motion
        self.socket.send(b"detect_motion")
        response = self.socket.recv(1024)
        return response

    def detect_temperature(self):
        # Send request to detect temperature
        self.socket.send(b"detect_temperature")
        response = self.socket.recv(1024)
        return response

    def detect_humidity(self):
        # Send request to detect humidity
        self.socket.send(b"detect_humidity")
        response = self.socket.recv(1024)
        return response

    def learn_patterns(self):
        # Send request to learn patterns
        self.socket.send(b"learn_patterns")
        response = self.socket.recv(1024)
        return response

    def predict_behavior(self):
        # Send request to predict behavior
        self.socket.send(b"predict_behavior")
        response = self.socket.recv(1024)
        return response
