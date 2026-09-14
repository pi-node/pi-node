import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Load historical price data
data = pd.read_csv('pi_coin_prices.csv')

# Data Preprocessing
# Fill missing values
data.fillna(method='ffill', inplace=True)

# Feature Engineering: Create additional features
data['price_change'] = data['price'].pct_change()  # Percentage change in price
data['volume_change'] = data['volume'].pct_change()  # Percentage change in volume
data['market_sentiment'] = data['market_sentiment'].fillna(0)  # Fill NaN with 0

# Drop rows with NaN values after feature engineering
data.dropna(inplace=True)

# Define features and target variable
X = data[['volume', 'market_sentiment', 'price_change', 'volume_change']]
y = data['price']

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build an advanced neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.2),  # Dropout layer to prevent overfitting
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)  # Output layer
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.1)

# Evaluate the model
loss, mae = model.evaluate(X_test, y_test)
print(f'Model Loss: {loss}, Mean Absolute Error: {mae}')

# Function to make predictions on new data
def predict_price(new_data):
    new_data_scaled = scaler.transform(new_data)
    predicted_price = model.predict(new_data_scaled)
    return predicted_price

# Example usage of the prediction function
# new_data should be a DataFrame with the same features as X
# new_data = pd.DataFrame({'volume': [1000], 'market_sentiment': [0.5], 'price_change': [0.01], 'volume_change': [0.02]})
# predicted_price = predict_price(new_data)
# print(f'Predicted Price: {predicted_price}')
