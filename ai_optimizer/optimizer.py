import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load node performance data
data = pd.read_csv('node_data.csv')

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data.drop('latency', axis=1), data['latency'], test_size=0.2, random_state=42)

# Train random forest regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Use model to predict optimal node configuration
optimal_config = model.predict(X_test)
