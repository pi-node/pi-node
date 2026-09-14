import socket

class AutonomousDroneClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def capture_image(self):
        # Send request to capture an image
        self.socket.send(b"capture_image")
        image = self.socket.recv(1024)
        return image

    def detect_obstacles(self, image):
        # Send request to detect obstacles
        self.socket.send(b"detect_obstacles")
        obstacles = self.socket.recv(1024)
        return obstacles

    def navigate(self, obstacles):
        # Send request to navigate
        self.socket.send(b"navigate")
        self.socket.send(obstacles)
