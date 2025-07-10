import logging
import os
import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Configure logging
logging.basicConfig(filename='anomaly_detector.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnomalyDetector:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.model = IsolationForest(contamination=self.config['contamination'])
        self.scaler = StandardScaler()

    def load_config(self, config_file):
        """Load configuration from a JSON file."""
        if os.path.exists(config_file):
            with open(config_file, 'r') as file:
                config = json.load(file)
                logging.info("Configuration loaded successfully.")
                return config
        else:
            logging.error(f"Configuration file {config_file} not found. Using default settings.")
            return {'contamination': 0.1}  # Default contamination rate

    def preprocess_data(self, data):
        """Preprocess the data for anomaly detection."""
        logging.info("Starting data preprocessing.")
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        logging.info("Data preprocessing completed.")
        return scaled_data

    def train_model(self, data):
        """Train the anomaly detection model."""
        logging.info("Training the anomaly detection model.")
        scaled_data = self.preprocess_data(data)
        self.model.fit(scaled_data)
        logging.info("Model training completed.")

    def detect_anomalies(self, data):
        """Detect anomalies in the provided data."""
        logging.info("Detecting anomalies.")
        scaled_data = self.scaler.transform(data)
        predictions = self.model.predict(scaled_data)
        anomalies = data[predictions == -1]
        logging.info(f"Detected {len(anomalies)} anomalies.")
        return anomalies

    def load_data(self, data_file):
        """Load data from a CSV file."""
        logging.info(f"Loading data from {data_file}.")
        data = pd.read_csv(data_file)
        logging.info("Data loaded successfully.")
        return data

if __name__ == "__main__":
    detector = AnomalyDetector()
    # Load data (replace 'data.csv' with your actual data file)
    data = detector.load_data('data.csv')
    # Train the model
    detector.train_model(data)
    # Detect anomalies
    anomalies = detector.detect_anomalies(data)
    print("Anomalies detected:")
    print(anomalies)
