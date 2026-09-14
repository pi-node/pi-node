import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class AutonomousDrone:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.classifier = RandomForestClassifier()

    def capture_image(self):
        # Capture an image from the drone's camera
        ret, frame = self.camera.read()
        return frame

    def detect_obstacles(self, image):
        # Detect obstacles in the image using computer vision
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        obstacles = []
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w)/h
            if area > 1000 and aspect_ratio > 2:
                obstacles.append((x, y, w, h))
        return obstacles

    def navigate(self, obstacles):
        # Navigate the drone using the detected obstacles
        for obstacle in obstacles:
            x, y, w, h = obstacle
            if x < 300:
                # Move left
                print("Moving left")
            elif x > 700:
                # Move right
                print("Moving right")
            elif y < 200:
                # Move up
                print("Moving up")
            elif y > 500:
                # Move down
                print("Moving down")
